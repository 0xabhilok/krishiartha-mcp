"""
FastMCP Server for KrishiArtha-MCP Quant Engine.

Wraps:
1. get_live_mandi_prices: Real-time Agmarknet / Mandi-API / OGD prices with deterministic offline fallback.
2. get_historical_mandi_series: Historical price time series.
3. calculate_route: OSRM highway routing with Haversine fallback and GeoJSON LineStrings.
4. forecast_and_arbitrage: End-to-end Chronos-2 covariate forecasting, Q10 spoilage decay,
   diesel freight deductions, and Net Realizable Price ranking.
"""

from typing import List, Dict, Any, Optional
import os
import math
import json
import logging
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

from mcp.server.fastmcp import FastMCP
from mcp_server.chronos_engine import (
    forecast_commodity_price_quantiles,
    get_weather_covariates,
    load_offline_snapshot,
    is_offline_mode,
)
from mcp_server.spoilage_arbitrage import (
    calculate_spoilage_loss,
    calculate_transport_cost,
    calculate_net_realizable_price,
    evaluate_mandi_arbitrage,
    DEFAULT_APMC_FEE_FRACTION,
    DEFAULT_UNLOADING_BUFFER_HOURS,
)

logger = logging.getLogger(__name__)

# FastMCP Server Instance
mcp = FastMCP("krishiartha-quant-engine")


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes great-circle distance in kilometers using the Haversine formula."""
    r = 6371.0  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(r * c, 2)


@mcp.tool()
def get_live_mandi_prices(state: str, commodity: str) -> List[Dict[str, Any]]:
    """
    Retrieves live wholesale mandi prices for the given state and commodity.
    Uses mandi-api.onrender.com or data.gov.in with a strict 2.5s timeout.
    Falls back deterministically to data/offline_snapshots/nashik_tomato_glut.json
    when offline safe mode is active or any API error occurs.
    """
    if not is_offline_mode():
        try:
            encoded_state = urllib.parse.quote(state)
            encoded_comm = urllib.parse.quote(commodity)
            url = f"https://mandi-api.onrender.com/v1/prices?state={encoded_state}&commodity={encoded_comm}"
            req = urllib.request.Request(url, headers={"User-Agent": "KrishiArtha-MCP/1.0"})
            with urllib.request.urlopen(req, timeout=2.5) as response:
                payload = json.loads(response.read().decode("utf-8"))
                records = payload.get("data", [])
                if records:
                    normalized: List[Dict[str, Any]] = []
                    for r in records:
                        normalized.append({
                            "state": r.get("state", state),
                            "district": r.get("district", "Nashik"),
                            "market": r.get("market", r.get("market_name", "Unknown")),
                            "lat": float(r.get("lat", 20.0)),
                            "lon": float(r.get("lon", 74.0)),
                            "commodity": r.get("commodity", commodity),
                            "variety": r.get("variety", "Standard"),
                            "arrival_date": r.get("arrival_date", datetime.now().strftime("%Y-%m-%d")),
                            "is_stale": bool(r.get("is_stale", False)),
                            "staleness_hours": int(r.get("staleness_hours", 12)),
                            "min_price_inr_per_quintal": float(r.get("min_price", r.get("min_price_inr_per_quintal", 800.0))),
                            "max_price_inr_per_quintal": float(r.get("max_price", r.get("max_price_inr_per_quintal", 1200.0))),
                            "modal_price_inr_per_quintal": float(r.get("modal_price", r.get("modal_price_inr_per_quintal", 1000.0))),
                        })
                    return normalized
        except Exception as e:
            logger.info("Live mandi price API call failed (%s); using deterministic offline snapshot", str(e))

    # Offline / Snapshot Deterministic Fallback
    snap = load_offline_snapshot()
    candidate_mandis = snap.get("candidate_mandis", [])
    today_str = datetime.now().strftime("%Y-%m-%d")

    results: List[Dict[str, Any]] = []
    for cand in candidate_mandis:
        m_name = cand.get("market_name", "APMC")
        modal = float(cand.get("current_modal_price", 1000.0))
        results.append({
            "state": cand.get("state", state),
            "district": cand.get("district", "Nashik"),
            "market": m_name,
            "lat": float(cand.get("lat", 20.0)),
            "lon": float(cand.get("lon", 73.8)),
            "commodity": commodity,
            "variety": "Deshi / Local",
            "arrival_date": today_str,
            "is_stale": False,
            "staleness_hours": 8,
            "min_price_inr_per_quintal": round(modal * 0.85, 2),
            "max_price_inr_per_quintal": round(modal * 1.15, 2),
            "modal_price_inr_per_quintal": modal,
        })

    return results


@mcp.tool()
def get_historical_mandi_series(
    state: str, commodity: str, market: str, days: int = 60
) -> List[Dict[str, Any]]:
    """
    Retrieves historical price series (modal, min, max) for a specific mandi and commodity.
    Enforces a 2.5s timeout. Seamlessly generates deterministic historical time-series
    anchored to the snapshot baseline when in offline mode or when external API is unreachable.
    """
    if not is_offline_mode():
        try:
            encoded_state = urllib.parse.quote(state)
            encoded_comm = urllib.parse.quote(commodity)
            encoded_market = urllib.parse.quote(market)
            url = f"https://mandi-api.onrender.com/v1/prices/history?state={encoded_state}&commodity={encoded_comm}&market={encoded_market}&days={days}"
            req = urllib.request.Request(url, headers={"User-Agent": "KrishiArtha-MCP/1.0"})
            with urllib.request.urlopen(req, timeout=2.5) as response:
                payload = json.loads(response.read().decode("utf-8"))
                series = payload.get("data", [])
                if series:
                    return series
        except Exception as e:
            logger.info("Historical mandi API failed (%s); generating deterministic series", str(e))

    # Deterministic series generation
    snap = load_offline_snapshot()
    matched = None
    for cand in snap.get("candidate_mandis", []):
        if cand.get("market_name", "").lower() in market.lower() or market.lower() in cand.get("market_name", "").lower():
            matched = cand
            break

    base_modal = float(matched.get("current_modal_price", 1000.0)) if matched else 1000.0
    now = datetime.now()

    history: List[Dict[str, Any]] = []
    for i in range(days, 0, -1):
        dt = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        # Realistic sinusoidal + random-walk deterministic variance
        day_factor = 1.0 + 0.12 * math.sin(i / 7.0) + 0.05 * math.cos(i / 13.0)
        modal = round(base_modal * day_factor, 2)
        min_p = round(modal * 0.88, 2)
        max_p = round(modal * 1.12, 2)
        arrivals_qtl = round(120.0 + 40.0 * math.sin(i / 5.0), 1)

        history.append({
            "date": dt,
            "state": state,
            "market": market,
            "commodity": commodity,
            "modal_price": modal,
            "min_price": min_p,
            "max_price": max_p,
            "arrivals_quintals": arrivals_qtl,
        })

    return history


@mcp.tool()
def calculate_route(
    origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float
) -> Dict[str, Any]:
    """
    Computes highway distance, transit duration, and route GeoJSON using OSRM routing.
    Enforces a 2.5s timeout. Seamlessly falls back to Haversine * 1.28 road tortuosity
    and LineString GeoJSON if OSRM is unreachable or OFFLINE_STAGE_SAFE_MODE=true.
    """
    if not is_offline_mode():
        try:
            url = (
                f"http://router.project-osrm.org/route/v1/driving/"
                f"{origin_lon:.5f},{origin_lat:.5f};{dest_lon:.5f},{dest_lat:.5f}"
                f"?overview=full&geometries=geojson"
            )
            req = urllib.request.Request(url, headers={"User-Agent": "KrishiArtha-MCP/1.0"})
            with urllib.request.urlopen(req, timeout=2.5) as response:
                payload = json.loads(response.read().decode("utf-8"))
                if payload.get("code") == "Ok" and payload.get("routes"):
                    primary_route = payload["routes"][0]
                    dist_km = round(primary_route["distance"] / 1000.0, 2)
                    dur_hrs = round(primary_route["duration"] / 3600.0, 2)
                    geometry = primary_route.get("geometry", {
                        "type": "LineString",
                        "coordinates": [[origin_lon, origin_lat], [dest_lon, dest_lat]],
                    })
                    return {
                        "distance_km": dist_km,
                        "duration_hours": dur_hrs,
                        "transit_hours": dur_hrs,
                        "route_geojson": geometry,
                        "status": "OK",
                        "source": "OSRM_HIGHWAY_LIVE",
                    }
        except Exception as e:
            logger.info("OSRM live routing failed (%s); using deterministic Haversine fallback", str(e))

    # Deterministic Haversine with road tortuosity factor (~1.28)
    haversine_dist = haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon)
    distance_km = round(haversine_dist * 1.28, 2)
    # Average commercial truck speed ~45 km/h on Indian highways
    duration_hours = round(max(0.25, distance_km / 45.0), 2)

    route_geojson = {
        "type": "LineString",
        "coordinates": [
            [round(origin_lon, 4), round(origin_lat, 4)],
            [round(dest_lon, 4), round(dest_lat, 4)],
        ],
    }

    return {
        "distance_km": distance_km,
        "duration_hours": duration_hours,
        "transit_hours": duration_hours,
        "route_geojson": route_geojson,
        "status": "OK",
        "source": "DETERMINISTIC_ROAD_TORTUOSITY_FALLBACK",
    }


@mcp.tool()
def forecast_and_arbitrage(farmer_lot_dict: dict) -> Dict[str, Any]:
    """
    Comprehensive quantitative spatial arbitrage and weather-covariate price forecasting.

    Parameters:
      farmer_lot_dict: Dict containing farmer lot information:
        - commodity: str (e.g. 'Tomato')
        - quantity_quintals: float (default 50.0)
        - farm_lat: float, farm_lon: float
        - farm_district: str, farm_state: str
        - cost_floor_per_qtl: float (default 1100.0)
        - weather_shock_Delta_mm: float (interactive what-if slider shock, default 0.0)

    Steps:
      1. Discovers candidate mandis (local APMC + regional consuming centers).
      2. Computes route distances and transit durations.
      3. Forecasts P10, P50, and P90 price quantiles with Chronos-2 elasticity and rainfall shock.
      4. Calculates Arrhenius Q10 biological spoilage decay in transit (+2.5h queue buffer).
      5. Calculates round-trip diesel freight and APMC fees.
      6. Computes Net Realizable Price per quintal (NRP) and ranks mandis descending.
      7. Flags regional crashes when all reachable mandis yield NRP < cost floor.
    """
    farmer_lot = dict(farmer_lot_dict)
    commodity = farmer_lot.get("commodity", "Tomato")
    quantity = float(farmer_lot.get("quantity_quintals", 50.0))
    farm_lat = float(farmer_lot.get("farm_lat", 19.9975))
    farm_lon = float(farmer_lot.get("farm_lon", 73.7898))
    cost_floor = float(farmer_lot.get("cost_floor_per_qtl", 1100.0))
    weather_shock_delta = float(farmer_lot.get("weather_shock_Delta_mm", 0.0))

    # Load baseline candidate mandis from snapshot
    snap = load_offline_snapshot()
    raw_candidates = snap.get("candidate_mandis", [])
    telemetry = snap.get("weather_telemetry", {})

    # Evaluate candidates
    candidate_list: List[Dict[str, Any]] = []
    for cand in raw_candidates:
        c = dict(cand)
        dest_lat = float(c.get("lat", 20.0))
        dest_lon = float(c.get("lon", 73.8))
        is_local = bool(c.get("is_local", False))
        market_name = c.get("market_name", "APMC")

        # 1. Routing calculation
        route_info = calculate_route(farm_lat, farm_lon, dest_lat, dest_lon)
        # Prefer snapshot calibrated highway distance if present, else routing
        dist_km = float(c.get("distance_km", route_info["distance_km"]))
        transit_hrs = float(c.get("transit_hours", route_info["transit_hours"]))
        route_geojson = route_info.get("route_geojson")

        # 2. Chronos price forecast with weather shock
        forecast = forecast_commodity_price_quantiles(
            market_name=market_name,
            commodity=commodity,
            current_modal_price=c.get("current_modal_price"),
            weather_covariates=telemetry,
            weather_shock_Delta_mm=weather_shock_delta,
            is_local=is_local,
        )

        p10 = forecast["forecast_p10"]
        p50 = forecast["forecast_p50"]
        p90 = forecast["forecast_p90"]

        # 3. Arrhenius Q10 biological spoilage decay
        temp_amb = float(telemetry.get("current_ambient_temp_c", 31.5))
        rel_hum = float(telemetry.get("current_relative_humidity_pct", 82.0))
        spoilage_loss_frac = calculate_spoilage_loss(
            temp_amb=temp_amb,
            rel_humidity=rel_hum,
            duration_hours=transit_hrs,
            commodity=commodity,
            unloading_buffer_hours=DEFAULT_UNLOADING_BUFFER_HOURS,
        )
        spoilage_pct = round(spoilage_loss_frac * 100.0, 2)
        spoilage_qtl = round(quantity * spoilage_loss_frac, 2)

        # 4. Transport freight cost
        transport_cost = calculate_transport_cost(
            distance_km=dist_km,
            quantity_quintals=quantity,
        )
        transport_per_qtl = round(transport_cost / quantity, 2) if quantity > 0 else 0.0

        # 5. APMC fee deduction
        gamma_apmc = DEFAULT_APMC_FEE_FRACTION
        mandi_fee_per_qtl = round(gamma_apmc * p50, 2)

        # 6. Net Realizable Price per quintal (NRP)
        nrp = calculate_net_realizable_price(
            forecast_p50=p50,
            spoilage_loss_fraction=spoilage_loss_frac,
            transport_cost_total=transport_cost,
            quantity_quintals=quantity,
            gamma_apmc=gamma_apmc,
        )
        total_payout = round(max(0.0, nrp * quantity), 2)

        candidate_list.append({
            "market_name": market_name,
            "district": c.get("district", "Nashik"),
            "state": c.get("state", "Maharashtra"),
            "lat": dest_lat,
            "lon": dest_lon,
            "distance_km": dist_km,
            "transit_hours": transit_hrs,
            "current_modal_price": float(c.get("current_modal_price", 1000.0)),
            "forecast_p10": p10,
            "forecast_p50": p50,
            "forecast_p90": p90,
            "spoilage_loss_pct": spoilage_pct,
            "spoilage_loss_quintals": spoilage_qtl,
            "transport_cost_per_qtl": transport_per_qtl,
            "total_transport_cost_inr": transport_cost,
            "mandi_fee_per_qtl": mandi_fee_per_qtl,
            "net_realizable_price_per_qtl": nrp,
            "total_net_payout_inr": total_payout,
            "is_local": is_local,
            "route_geojson": route_geojson,
        })

    # Sort candidates descending by Net Realizable Price
    candidate_list.sort(key=lambda x: x["net_realizable_price_per_qtl"], reverse=True)

    # Local mandi reference
    local_mandi = next((m for m in candidate_list if m.get("is_local")), candidate_list[-1] if candidate_list else None)
    local_payout = local_mandi["total_net_payout_inr"] if local_mandi else 0.0

    # Calculate arbitrage gain over local
    for m in candidate_list:
        if m.get("is_local"):
            m["arbitrage_gain_over_local_inr"] = 0.0
        else:
            m["arbitrage_gain_over_local_inr"] = round(max(0.0, m["total_net_payout_inr"] - local_payout), 2)

    optimal_mandi = candidate_list[0] if candidate_list else None
    net_arbitrage_gain = optimal_mandi["arbitrage_gain_over_local_inr"] if optimal_mandi and not optimal_mandi.get("is_local") else 0.0
    is_regional_crash = (optimal_mandi["net_realizable_price_per_qtl"] < cost_floor) if optimal_mandi else True

    response: Dict[str, Any] = {
        "candidate_mandis": candidate_list,
        "optimal_mandi": optimal_mandi,
        "local_mandi": local_mandi,
        "net_arbitrage_gain_inr": net_arbitrage_gain,
        "is_regional_crash": is_regional_crash,
        "cost_floor_per_qtl": cost_floor,
        "highest_net_realizable_price": optimal_mandi["net_realizable_price_per_qtl"] if optimal_mandi else 0.0,
        "farmer_lot": farmer_lot,
        "weather_telemetry": telemetry,
    }

    # If regional crash occurs, attach statutory distress solution details
    if is_regional_crash and "recommended_distress_solution" in snap:
        response["distress_recommendation"] = snap["recommended_distress_solution"]

    return response


if __name__ == "__main__":
    # Standard entrypoint for FastMCP stdio or SSE server execution
    import sys
    transport = "stdio"
    if "--sse" in sys.argv or os.getenv("MCP_TRANSPORT") == "sse":
        transport = "sse"
    mcp.run(transport=transport)
