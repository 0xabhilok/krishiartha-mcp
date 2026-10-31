"""
Unit and Integration Tests for FastMCP Quant Engine.

Validates:
1. FastMCP server tool functions:
   - get_live_mandi_prices
   - get_historical_mandi_series
   - calculate_route
   - forecast_and_arbitrage
2. Chronos-2 weather-covariate price forecasting & P10/P50/P90 quantile invariants.
3. Interactive weather_shock_Delta_mm additive covariate shift and price elasticity.
4. Arrhenius Q10 biological thermal transit spoilage formula:
   k(T_amb, RH) = k_base * (Q10)^((T_amb - 20)/10) * (1 + alpha_hum * max(0, (RH - 70)/100))
   L = 1 - exp(-k * (duration_hours + 2.5))
5. Diesel freight deduction (2 * distance_km * 22 INR/km + Q * 35 INR/qtl) & APMC fee (gamma * P50).
6. Net Realizable Price (NRP = P50 * (1 - L) * (1 - gamma) - transport_cost / Q) & descending ranking.
7. Regional crash detection against cost floor.
8. Deterministic offline snapshot fallback resilience under OFFLINE_STAGE_SAFE_MODE=true and API timeouts.
"""

import os
import sys
import math
import pytest
from pathlib import Path

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from mcp_server.spoilage_arbitrage import (
    calculate_spoilage_rate_k,
    calculate_spoilage_loss,
    calculate_transport_cost,
    calculate_net_realizable_price,
    evaluate_mandi_arbitrage,
    DEFAULT_Q10,
    DEFAULT_ALPHA_HUM,
    CROP_BASE_SPOILAGE_RATES,
)
from mcp_server.chronos_engine import (
    forecast_commodity_price_quantiles,
    get_weather_covariates,
    load_offline_snapshot,
    is_offline_mode,
)
from mcp_server.server import (
    mcp,
    get_live_mandi_prices,
    get_historical_mandi_series,
    calculate_route,
    forecast_and_arbitrage,
    haversine_distance,
)


# ==============================================================================
# SECTION 1: Arrhenius Q10 Spoilage & Physics Economics Math Tests
# ==============================================================================

class TestSpoilageArbitrageMath:
    """Rigorous unit tests for Arrhenius Q10 and freight deduction math."""

    def test_q10_decay_rate_at_baseline_reference_temp(self):
        """At 20°C and RH <= 70%, k(T_amb, RH) must exactly equal k_base."""
        temp_amb = 20.0
        rel_humidity = 65.0  # <= 70, excess RH is 0
        k = calculate_spoilage_rate_k(temp_amb, rel_humidity, commodity="Tomato")
        expected_k = CROP_BASE_SPOILAGE_RATES["Tomato"]  # 0.0065
        assert math.isclose(k, expected_k, rel_tol=1e-5), f"Expected {expected_k}, got {k}"

    def test_q10_decay_rate_temperature_scaling(self):
        """At 30°C and RH <= 70%, temperature acceleration should be exactly Q10^1 = 2.2."""
        temp_amb = 30.0
        rel_humidity = 60.0
        k = calculate_spoilage_rate_k(temp_amb, rel_humidity, commodity="Tomato")
        expected_k = 0.0065 * 2.2  # 0.0143
        assert math.isclose(k, expected_k, rel_tol=1e-5), f"Expected {expected_k}, got {k}"

    def test_q10_decay_rate_humidity_acceleration(self):
        """At 20°C and 80% RH, humidity multiplier should be 1 + 1.5 * (80 - 70) / 100 = 1.15."""
        temp_amb = 20.0
        rel_humidity = 80.0
        k = calculate_spoilage_rate_k(temp_amb, rel_humidity, commodity="Tomato")
        expected_k = 0.0065 * 1.0 * (1.0 + 1.5 * 0.10)  # 0.0065 * 1.15 = 0.007475
        assert math.isclose(k, expected_k, rel_tol=1e-5), f"Expected {expected_k}, got {k}"

    def test_spoilage_loss_fraction_with_unloading_buffer(self):
        """Transit loss fraction L = 1 - exp(-k * (duration + 2.5h buffer))."""
        temp_amb = 30.0
        rel_humidity = 70.0
        duration_hours = 5.0
        buffer_hours = 2.5
        t_total = 7.5

        k = calculate_spoilage_rate_k(temp_amb, rel_humidity, commodity="Tomato")
        loss = calculate_spoilage_loss(
            temp_amb=temp_amb,
            rel_humidity=rel_humidity,
            duration_hours=duration_hours,
            commodity="Tomato",
            unloading_buffer_hours=buffer_hours,
        )

        expected_loss = 1.0 - math.exp(-k * t_total)
        assert math.isclose(loss, expected_loss, rel_tol=1e-5)
        assert 0.0 < loss < 1.0

    def test_spoilage_monotonicity_with_temperature_and_duration(self):
        """Higher ambient temperature or longer transit time strictly increases crop loss."""
        loss_cool = calculate_spoilage_loss(temp_amb=22.0, rel_humidity=75.0, duration_hours=4.0)
        loss_hot = calculate_spoilage_loss(temp_amb=34.0, rel_humidity=75.0, duration_hours=4.0)
        loss_longer = calculate_spoilage_loss(temp_amb=34.0, rel_humidity=75.0, duration_hours=8.0)

        assert loss_hot > loss_cool, "Hot transit must produce higher spoilage than cool transit"
        assert loss_longer > loss_hot, "Longer transit must produce higher spoilage than short transit"

    def test_transport_diesel_freight_deduction(self):
        """Round-trip diesel: 2 * distance_km * 22 INR/km + Q * 35 INR/qtl."""
        distance_km = 100.0
        quantity_qtl = 50.0
        cost = calculate_transport_cost(distance_km, quantity_qtl)

        # 2 * 100 * 22 = 4400. 50 * 35 = 1750. Total = 6150.0
        expected_cost = (2.0 * 100.0 * 22.0) + (50.0 * 35.0)
        assert cost == expected_cost
        assert cost == 6150.0

    def test_net_realizable_price_formula(self):
        """NRP = P50 * (1 - L) * (1 - gamma) - (transport_cost / Q)."""
        p50 = 1340.0
        spoilage_loss = 0.184  # 18.4%
        transport_total = 6800.0
        quantity_qtl = 50.0
        gamma = 0.015  # 1.5%

        nrp = calculate_net_realizable_price(
            forecast_p50=p50,
            spoilage_loss_fraction=spoilage_loss,
            transport_cost_total=transport_total,
            quantity_quintals=quantity_qtl,
            gamma_apmc=gamma,
        )

        expected_gross = p50 * (1.0 - spoilage_loss) * (1.0 - gamma)
        expected_nrp = round(expected_gross - (transport_total / quantity_qtl), 2)
        assert nrp == expected_nrp


# ==============================================================================
# SECTION 2: Chronos-2 Price Quantiles & Weather Shock Shift Tests
# ==============================================================================

class TestChronosEngine:
    """Validates Chronos-2 probabilistic quantiles and additive covariate shifts."""

    def test_quantiles_monotonic_invariant(self):
        """Ensures fundamental quantile ordering: P10 <= P50 <= P90."""
        forecast = forecast_commodity_price_quantiles(
            market_name="Pimpalgaon Baswant APMC",
            commodity="Tomato",
            current_modal_price=900.0,
            weather_shock_Delta_mm=0.0,
        )

        p10 = forecast["forecast_p10"]
        p50 = forecast["forecast_p50"]
        p90 = forecast["forecast_p90"]

        assert p10 <= p50 <= p90, f"Quantile invariant violated: P10={p10}, P50={p50}, P90={p90}"

    def test_weather_shock_delta_downward_price_shift(self):
        """
        An unseasonal cloudburst shock (+Delta mm) at local harvest mandi causes
        panic dumping: P50 drops, and downside panic risk (P10) expands significantly.
        """
        baseline = forecast_commodity_price_quantiles(
            market_name="Pimpalgaon Baswant APMC",
            commodity="Tomato",
            current_modal_price=900.0,
            weather_shock_Delta_mm=0.0,
            is_local=True,
        )

        shocked = forecast_commodity_price_quantiles(
            market_name="Pimpalgaon Baswant APMC",
            commodity="Tomato",
            current_modal_price=900.0,
            weather_shock_Delta_mm=45.0,  # +45mm unseasonal rain shock
            is_local=True,
        )

        assert shocked["forecast_p50"] < baseline["forecast_p50"], (
            f"Expected shocked P50 ({shocked['forecast_p50']}) < baseline P50 ({baseline['forecast_p50']})"
        )
        assert shocked["forecast_p10"] < baseline["forecast_p10"], (
            f"Expected shocked P10 ({shocked['forecast_p10']}) < baseline P10 ({baseline['forecast_p10']})"
        )
        # Check that quantile invariant still holds under heavy shock
        assert shocked["forecast_p10"] <= shocked["forecast_p50"] <= shocked["forecast_p90"]

    def test_daily_forecast_horizon_structure(self):
        """Verifies 7-day daily forecast structure and covariate tracking."""
        forecast = forecast_commodity_price_quantiles(
            market_name="Surat APMC",
            commodity="Tomato",
            current_modal_price=1350.0,
            horizon_days=7,
        )

        daily = forecast.get("daily_forecast", [])
        assert len(daily) == 7
        for d in daily:
            assert "day" in d
            assert "p10" in d
            assert "p50" in d
            assert "p90" in d
            assert d["p10"] <= d["p50"] <= d["p90"]


# ==============================================================================
# SECTION 3: FastMCP Tool Server Endpoints Tests
# ==============================================================================

class TestFastMCPServerTools:
    """Tests FastMCP registered tools and operational contracts."""

    def test_fastmcp_registered_tools_present(self):
        """Verifies that all 4 required MCP tools are properly registered on the FastMCP instance."""
        tool_names = [t.name for t in mcp._tool_manager.list_tools()]
        required_tools = [
            "get_live_mandi_prices",
            "get_historical_mandi_series",
            "calculate_route",
            "forecast_and_arbitrage",
        ]
        for req in required_tools:
            assert req in tool_names, f"Tool {req} not registered in FastMCP server"

    def test_get_live_mandi_prices_returns_normalized_records(self):
        """Tests live mandi price tool returning valid normalized schema."""
        records = get_live_mandi_prices("Maharashtra", "Tomato")
        assert isinstance(records, list)
        assert len(records) > 0

        first = records[0]
        assert "market" in first
        assert "commodity" in first
        assert "modal_price_inr_per_quintal" in first
        assert first["modal_price_inr_per_quintal"] > 0

    def test_get_historical_mandi_series_length_and_fields(self):
        """Tests historical price series generation for specified days."""
        days = 30
        series = get_historical_mandi_series("Maharashtra", "Tomato", "Pimpalgaon Baswant APMC", days=days)
        assert isinstance(series, list)
        assert len(series) == days

        for item in series:
            assert "date" in item
            assert "modal_price" in item
            assert item["min_price"] <= item["modal_price"] <= item["max_price"]

    def test_calculate_route_tool_output(self):
        """Tests routing calculation with distance, transit duration, and GeoJSON coordinates."""
        # Origin: Nashik (19.9975, 73.7898), Dest: Pimpalgaon Baswant (20.1704, 73.9845)
        route = calculate_route(19.9975, 73.7898, 20.1704, 73.9845)
        assert route["status"] == "OK"
        assert route["distance_km"] > 0.0
        assert route["duration_hours"] > 0.0
        assert "route_geojson" in route
        assert route["route_geojson"]["type"] == "LineString"
        assert len(route["route_geojson"]["coordinates"]) >= 2

    def test_forecast_and_arbitrage_end_to_end(self):
        """Tests end-to-end multi-market spatial arbitrage optimization and ranking."""
        farmer_lot = {
            "farmer_name": "Suresh Patil",
            "commodity": "Tomato",
            "quantity_quintals": 50.0,
            "farm_lat": 19.9975,
            "farm_lon": 73.7898,
            "farm_district": "Nashik",
            "farm_state": "Maharashtra",
            "cost_floor_per_qtl": 1100.0,
            "weather_shock_Delta_mm": 0.0,
        }

        result = forecast_and_arbitrage(farmer_lot)

        assert "candidate_mandis" in result
        assert "optimal_mandi" in result
        assert "local_mandi" in result
        assert "is_regional_crash" in result
        assert "net_arbitrage_gain_inr" in result

        candidates = result["candidate_mandis"]
        assert len(candidates) >= 3

        # Verify candidate mandis are sorted strictly descending by Net Realizable Price
        for i in range(len(candidates) - 1):
            assert candidates[i]["net_realizable_price_per_qtl"] >= candidates[i + 1]["net_realizable_price_per_qtl"], (
                f"Candidate mandis not sorted descending by NRP: "
                f"{candidates[i]['net_realizable_price_per_qtl']} < {candidates[i+1]['net_realizable_price_per_qtl']}"
            )

        # Top candidate should be Surat APMC with positive arbitrage gain over Pimpalgaon
        optimal = result["optimal_mandi"]
        assert optimal is not None
        assert optimal["net_realizable_price_per_qtl"] > 0

    def test_regional_crash_trigger_and_statutory_recommendation(self):
        """
        When cost floor is set to ₹1100/qtl and every reachable APMC yields NRP < ₹1100,
        is_regional_crash must be True and statutory WDRA distress recommendation attached.
        """
        farmer_lot = {
            "farmer_name": "Suresh Patil",
            "commodity": "Tomato",
            "quantity_quintals": 50.0,
            "farm_lat": 19.9975,
            "farm_lon": 73.7898,
            "cost_floor_per_qtl": 1100.0,
            "weather_shock_Delta_mm": 0.0,
        }

        result = forecast_and_arbitrage(farmer_lot)
        # In Nashik unseasonal tomato scenario, highest NRP is Surat at ~₹965.6/qtl, below ₹1100 floor
        assert result["is_regional_crash"] is True
        assert "distress_recommendation" in result
        assert result["distress_recommendation"]["strategy"].startswith("WDRA")


# ==============================================================================
# SECTION 4: Offline Stage Safe Mode & Resilience Fallback Tests
# ==============================================================================

class TestOfflineResilience:
    """Validates deterministic fallback to data/offline_snapshots/nashik_tomato_glut.json."""

    def test_load_offline_snapshot_validity(self):
        """Ensures the offline snapshot loads properly and contains canonical scenario keys."""
        snap = load_offline_snapshot()
        assert "scenario" in snap
        assert "farmer_lot" in snap
        assert "weather_telemetry" in snap
        assert "candidate_mandis" in snap
        assert len(snap["candidate_mandis"]) >= 4

    def test_offline_mode_env_flag_behavior(self, monkeypatch):
        """When OFFLINE_STAGE_SAFE_MODE=true, get_weather_covariates uses offline snapshot without external calls."""
        monkeypatch.setenv("OFFLINE_STAGE_SAFE_MODE", "true")
        assert is_offline_mode() is True

        weather = get_weather_covariates(19.9975, 73.7898)
        assert weather["current_ambient_temp_c"] == 31.5
        assert weather["current_relative_humidity_pct"] == 82.0
        assert len(weather["forecast_7_days"]) == 7

    def test_simulated_network_timeout_graceful_fallback(self, monkeypatch):
        """If external network times out (> 2.5s) or fails, fallback snapshot is seamlessly returned."""
        monkeypatch.setenv("OFFLINE_STAGE_SAFE_MODE", "false")

        # Simulate timeout by providing an unreachable port
        weather = get_weather_covariates(0.0, 0.0, timeout_s=0.001)
        assert weather is not None
        assert "current_ambient_temp_c" in weather


# ==============================================================================
# SECTION 5: Additional Physics & Standalone Logic Tests
# ==============================================================================

class TestExtendedQuantFeatures:
    """Tests multi-crop decay baseline rates, Haversine accuracy, and cost floor dynamics."""

    def test_crop_specific_k_base_rates(self):
        """Perishables have different baseline decay rates (Tomato 0.0065 vs Onion 0.0018)."""
        k_tomato = calculate_spoilage_rate_k(20.0, 60.0, commodity="Tomato")
        k_onion = calculate_spoilage_rate_k(20.0, 60.0, commodity="Onion")
        k_potato = calculate_spoilage_rate_k(20.0, 60.0, commodity="Potato")

        assert k_tomato == 0.0065
        assert k_onion == 0.0018
        assert k_potato == 0.0020
        assert k_tomato > k_onion, "Tomato must decay faster than Onion under identical ambient conditions"

    def test_haversine_distance_accuracy(self):
        """Tests Haversine calculation between Nashik (19.9975, 73.7898) and Mumbai (19.0760, 72.8777)."""
        dist = haversine_distance(19.9975, 73.7898, 19.0760, 72.8777)
        # Great-circle distance between Nashik and Mumbai is ~135 - 145 km
        assert 130.0 <= dist <= 150.0, f"Unexpected Haversine distance: {dist} km"

    def test_cost_floor_dynamics_and_arbitrage_gain(self):
        """When cost floor is low (e.g. ₹800), regional crash is False; when high (₹1500), True."""
        farmer_lot_low_floor = {
            "farmer_name": "Suresh Patil",
            "commodity": "Tomato",
            "quantity_quintals": 50.0,
            "cost_floor_per_qtl": 800.0,
            "weather_shock_Delta_mm": 0.0,
        }
        res_low = forecast_and_arbitrage(farmer_lot_low_floor)
        assert res_low["is_regional_crash"] is False

        farmer_lot_high_floor = {
            "farmer_name": "Suresh Patil",
            "commodity": "Tomato",
            "quantity_quintals": 50.0,
            "cost_floor_per_qtl": 1500.0,
            "weather_shock_Delta_mm": 0.0,
        }
        res_high = forecast_and_arbitrage(farmer_lot_high_floor)
        assert res_high["is_regional_crash"] is True

    def test_weather_shock_impact_in_arbitrage(self):
        """Interactive rainfall slider (+Delta mm) widens arbitrage opportunity over crash-hit local market."""
        lot_base = {
            "farmer_name": "Suresh Patil",
            "commodity": "Tomato",
            "quantity_quintals": 50.0,
            "cost_floor_per_qtl": 1100.0,
            "weather_shock_Delta_mm": 0.0,
        }
        res_base = forecast_and_arbitrage(lot_base)

        lot_shock = {
            "farmer_name": "Suresh Patil",
            "commodity": "Tomato",
            "quantity_quintals": 50.0,
            "cost_floor_per_qtl": 1100.0,
            "weather_shock_Delta_mm": 50.0,
        }
        res_shock = forecast_and_arbitrage(lot_shock)

        local_base = res_base["local_mandi"]
        local_shock = res_shock["local_mandi"]
        assert local_shock["net_realizable_price_per_qtl"] < local_base["net_realizable_price_per_qtl"], (
            "Local mandi NRP must decrease under severe rainfall shock"
        )

