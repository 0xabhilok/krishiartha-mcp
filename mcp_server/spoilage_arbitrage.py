"""
Arrhenius Q10 Biological Transit Spoilage & Spatial Arbitrage Engine.

Implements:
1. Temperature and humidity dependent microbial/respiration decay rate k(T_amb, RH).
2. Transit spoilage loss fraction L = 1 - exp(-k * t_transit) with +2.5h unloading buffer.
3. Round-trip diesel freight and handling cost: 2 * distance_km * 22 INR/km + Q * 35 INR/qtl.
4. APMC mandi fee deduction: gamma_APMC * P50.
5. Net Realizable Price (NRP) per quintal and total net payout.
6. Multi-market ranking descending by NRP and regional crash detection against cost floor.
"""

from typing import List, Dict, Any, Optional
import math

# Baseline hourly loss rates at 20°C (k_base)
CROP_BASE_SPOILAGE_RATES = {
    "Tomato": 0.0065,
    "Tomato (Deshi)": 0.0065,
    "Tomato (Hybrid)": 0.0060,
    "Onion": 0.0018,
    "Potato": 0.0020,
    "Green Chilli": 0.0050,
    "Banana": 0.0055,
    "Leafy Greens": 0.0050,
}
DEFAULT_K_BASE = 0.0065
DEFAULT_Q10 = 2.2
DEFAULT_ALPHA_HUM = 1.5
DEFAULT_DIESEL_RATE_PER_KM = 22.0      # ₹22 / km round-trip mini-truck rate
DEFAULT_LOADING_FEE_PER_QTL = 35.0     # ₹35 / quintal loading/unloading (hamali)
DEFAULT_APMC_FEE_FRACTION = 0.015      # 1.5% APMC market cess & handling fee
DEFAULT_UNLOADING_BUFFER_HOURS = 2.5   # 2.5 hours mandi queuing and unloading penalty


def calculate_spoilage_rate_k(
    temp_amb: float,
    rel_humidity: float,
    commodity: str = "Tomato",
    q10: float = DEFAULT_Q10,
    alpha_hum: float = DEFAULT_ALPHA_HUM,
    k_base: Optional[float] = None,
) -> float:
    """
    Computes Arrhenius Q10 biological spoilage decay rate constant k(T_amb, RH).

    Formula:
      k(T_amb, RH) = k_base * (Q10)^((T_amb - 20.0) / 10.0) * (1 + alpha_hum * max(0, (RH - 70) / 100))

    Parameters:
      temp_amb: Ambient temperature in °C
      rel_humidity: Relative humidity in % [0 - 100]
      commodity: Crop commodity name
      q10: Temperature sensitivity coefficient (default 2.2)
      alpha_hum: Moisture rot multiplier (default 1.5)
      k_base: Optional explicit baseline rate; if None, derived from commodity lookup

    Returns:
      Decay rate constant k (per hour)
    """
    if k_base is None:
        k_base = CROP_BASE_SPOILAGE_RATES.get(commodity, DEFAULT_K_BASE)

    # Temperature acceleration factor
    temp_factor = math.pow(q10, (temp_amb - 20.0) / 10.0)

    # Humidity acceleration factor (kicks in above 70% RH)
    excess_rh = max(0.0, (rel_humidity - 70.0) / 100.0)
    humidity_factor = 1.0 + alpha_hum * excess_rh

    k = k_base * temp_factor * humidity_factor
    return k


def calculate_spoilage_loss(
    temp_amb: float,
    rel_humidity: float,
    duration_hours: float,
    commodity: str = "Tomato",
    unloading_buffer_hours: float = DEFAULT_UNLOADING_BUFFER_HOURS,
    q10: float = DEFAULT_Q10,
    alpha_hum: float = DEFAULT_ALPHA_HUM,
    k_base: Optional[float] = None,
) -> float:
    """
    Computes marketable weight loss fraction L during highway transit + mandi queuing.

    Formula:
      t_transit = duration_hours + unloading_buffer_hours
      L = 1 - exp(-k * t_transit)

    Returns:
      Loss fraction L in [0.0, 1.0)
    """
    k = calculate_spoilage_rate_k(
        temp_amb=temp_amb,
        rel_humidity=rel_humidity,
        commodity=commodity,
        q10=q10,
        alpha_hum=alpha_hum,
        k_base=k_base,
    )
    t_transit = max(0.0, duration_hours + unloading_buffer_hours)
    loss_fraction = 1.0 - math.exp(-k * t_transit)
    return min(max(loss_fraction, 0.0), 1.0)


def calculate_transport_cost(
    distance_km: float,
    quantity_quintals: float,
    rate_diesel_per_km: float = DEFAULT_DIESEL_RATE_PER_KM,
    loading_fee_per_qtl: float = DEFAULT_LOADING_FEE_PER_QTL,
    round_trip: bool = True,
) -> float:
    """
    Computes total transport & handling freight in INR.

    Formula:
      C_transport = (2 * distance_km if round_trip else distance_km) * rate_diesel_per_km
                    + quantity_quintals * loading_fee_per_qtl
    """
    multiplier = 2.0 if round_trip else 1.0
    diesel_freight = multiplier * distance_km * rate_diesel_per_km
    loading_handling = max(0.0, quantity_quintals) * loading_fee_per_qtl
    return round(diesel_freight + loading_handling, 2)


def calculate_net_realizable_price(
    forecast_p50: float,
    spoilage_loss_fraction: float,
    transport_cost_total: float,
    quantity_quintals: float,
    gamma_apmc: float = DEFAULT_APMC_FEE_FRACTION,
) -> float:
    """
    Computes Net Realizable Price per quintal (NRP) in INR/qtl.

    Formula:
      NRP = P50 * (1 - L) * (1 - gamma_APMC) - (transport_cost / Q)
    """
    if quantity_quintals <= 0:
        return 0.0
    transport_cost_per_qtl = transport_cost_total / quantity_quintals
    realizable_gross = forecast_p50 * (1.0 - spoilage_loss_fraction) * (1.0 - gamma_apmc)
    nrp = realizable_gross - transport_cost_per_qtl
    return round(nrp, 2)


def evaluate_mandi_arbitrage(
    farmer_lot: Dict[str, Any],
    candidate_mandis: List[Dict[str, Any]],
    weather_telemetry: Optional[Dict[str, Any]] = None,
    default_gamma_apmc: float = DEFAULT_APMC_FEE_FRACTION,
    unloading_buffer_hours: float = DEFAULT_UNLOADING_BUFFER_HOURS,
) -> Dict[str, Any]:
    """
    Evaluates multiple candidate mandis for a given farmer lot, applying:
    - Arrhenius Q10 biological transit spoilage decay
    - Round-trip diesel freight and loading deductions
    - Statutory APMC fee deductions
    - Net Realizable Price ranking descending by NRP
    - Regional crash threshold comparison against cost_floor_per_qtl

    Returns structured arbitrage analysis dictionary.
    """
    quantity = float(farmer_lot.get("quantity_quintals", 50.0))
    commodity = farmer_lot.get("commodity", "Tomato")
    cost_floor = float(farmer_lot.get("cost_floor_per_qtl", 1100.0))

    # Ambient telemetry defaults (Nashik unseasonal glut baseline)
    temp_amb = 31.5
    rel_humidity = 82.0
    if weather_telemetry:
        temp_amb = float(weather_telemetry.get("current_ambient_temp_c", temp_amb))
        rel_humidity = float(weather_telemetry.get("current_relative_humidity_pct", rel_humidity))

    evaluated_mandis: List[Dict[str, Any]] = []

    # First pass: compute metrics for each candidate
    for mandi in candidate_mandis:
        m_copy = dict(mandi)
        dist_km = float(m_copy.get("distance_km", 0.0))
        transit_hrs = float(m_copy.get("transit_hours", 0.0))
        is_local = bool(m_copy.get("is_local", False))
        modal_price = float(m_copy.get("current_modal_price", 1000.0))

        # Price forecasts
        p50 = float(m_copy.get("forecast_p50", modal_price))
        p10 = float(m_copy.get("forecast_p10", p50 * 0.8))
        p90 = float(m_copy.get("forecast_p90", p50 * 1.15))

        gamma = float(m_copy.get("apmc_fee_fraction", default_gamma_apmc))

        # Check if candidate already has precomputed values from offline snapshot
        has_precomputed = (
            "net_realizable_price_per_qtl" in m_copy
            and "spoilage_loss_pct" in m_copy
            and "total_transport_cost_inr" in m_copy
        )

        if not has_precomputed:
            # Calculate spoilage loss fraction
            spoilage_frac = calculate_spoilage_loss(
                temp_amb=temp_amb,
                rel_humidity=rel_humidity,
                duration_hours=transit_hrs,
                commodity=commodity,
                unloading_buffer_hours=unloading_buffer_hours,
            )
            spoilage_pct = round(spoilage_frac * 100.0, 2)
            spoilage_qtl = round(quantity * spoilage_frac, 2)

            # Transport cost
            total_trans_cost = calculate_transport_cost(
                distance_km=dist_km,
                quantity_quintals=quantity,
            )
            trans_cost_per_qtl = round(total_trans_cost / quantity, 2) if quantity > 0 else 0.0

            # Mandi fee per qtl
            mandi_fee_per_qtl = round(gamma * p50, 2)

            # Net realizable price
            nrp = calculate_net_realizable_price(
                forecast_p50=p50,
                spoilage_loss_fraction=spoilage_frac,
                transport_cost_total=total_trans_cost,
                quantity_quintals=quantity,
                gamma_apmc=gamma,
            )

            total_payout = round(max(0.0, nrp * quantity), 2)

            m_copy["spoilage_loss_pct"] = spoilage_pct
            m_copy["spoilage_loss_quintals"] = spoilage_qtl
            m_copy["transport_cost_per_qtl"] = trans_cost_per_qtl
            m_copy["total_transport_cost_inr"] = total_trans_cost
            m_copy["mandi_fee_per_qtl"] = mandi_fee_per_qtl
            m_copy["net_realizable_price_per_qtl"] = nrp
            m_copy["total_net_payout_inr"] = total_payout
        else:
            # Ensure proper typing for precomputed fields
            m_copy["net_realizable_price_per_qtl"] = float(m_copy["net_realizable_price_per_qtl"])
            m_copy["spoilage_loss_pct"] = float(m_copy["spoilage_loss_pct"])
            m_copy["total_transport_cost_inr"] = float(m_copy["total_transport_cost_inr"])
            m_copy["transport_cost_per_qtl"] = float(m_copy.get("transport_cost_per_qtl", m_copy["total_transport_cost_inr"] / quantity))
            m_copy["total_net_payout_inr"] = float(m_copy.get("total_net_payout_inr", m_copy["net_realizable_price_per_qtl"] * quantity))
            m_copy["mandi_fee_per_qtl"] = float(m_copy.get("mandi_fee_per_qtl", round(gamma * p50, 2)))
            m_copy["spoilage_loss_quintals"] = float(m_copy.get("spoilage_loss_quintals", round(quantity * (m_copy["spoilage_loss_pct"] / 100.0), 2)))

        m_copy["forecast_p10"] = p10
        m_copy["forecast_p50"] = p50
        m_copy["forecast_p90"] = p90
        m_copy["current_modal_price"] = modal_price
        m_copy["distance_km"] = dist_km
        m_copy["transit_hours"] = transit_hrs
        m_copy["is_local"] = is_local

        evaluated_mandis.append(m_copy)

    # Sort descending by Net Realizable Price per quintal
    evaluated_mandis.sort(key=lambda x: x["net_realizable_price_per_qtl"], reverse=True)

    # Identify local mandi
    local_mandi = next((m for m in evaluated_mandis if m.get("is_local")), None)
    if not local_mandi and evaluated_mandis:
        # Lowest distance mandi is local fallback
        local_mandi = min(evaluated_mandis, key=lambda x: x.get("distance_km", 0.0))

    local_payout = local_mandi["total_net_payout_inr"] if local_mandi else 0.0

    # Calculate arbitrage gain over local mandi for each candidate
    for m in evaluated_mandis:
        if m.get("is_local"):
            m["arbitrage_gain_over_local_inr"] = 0.0
        else:
            diff = round(max(0.0, m["total_net_payout_inr"] - local_payout), 2)
            m["arbitrage_gain_over_local_inr"] = diff

    optimal_mandi = evaluated_mandis[0] if evaluated_mandis else None
    max_nrp = optimal_mandi["net_realizable_price_per_qtl"] if optimal_mandi else 0.0
    net_arbitrage_gain = (
        optimal_mandi["arbitrage_gain_over_local_inr"]
        if optimal_mandi and not optimal_mandi.get("is_local")
        else 0.0
    )

    # Regional crash detection: True if highest attainable NRP < cost floor
    is_regional_crash = max_nrp < cost_floor

    return {
        "candidate_mandis": evaluated_mandis,
        "optimal_mandi": optimal_mandi,
        "local_mandi": local_mandi,
        "net_arbitrage_gain_inr": net_arbitrage_gain,
        "is_regional_crash": is_regional_crash,
        "cost_floor_per_qtl": cost_floor,
        "highest_net_realizable_price": max_nrp,
        "farmer_lot": farmer_lot,
        "weather_telemetry": weather_telemetry or {
            "current_ambient_temp_c": temp_amb,
            "current_relative_humidity_pct": rel_humidity,
        },
    }
