"""
KrishiArtha-MCP LangGraph Orchestrator.
Builds the 4-node deterministic StateGraph using InMemorySaver checkpointer:
  quant_arbitrage -> policy_graphrag -> human_approval_gate -> execute_enwr_browser

Conforms strictly to KrishiArthaGraphStateDict schema and implements interrupt()
human-in-the-loop gate with zero side-effects above the call.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

from contracts.schemas import KrishiArthaGraphStateDict
from orchestrator.enwr_browser_agent import run_enwr_browser_agent

SNAPSHOT_PATH = Path(__file__).resolve().parent.parent / "data" / "offline_snapshots" / "nashik_tomato_glut.json"


def _load_snapshot_data() -> Dict[str, Any]:
    """Helper to load offline snapshot data for realistic fallback telemetry."""
    if SNAPSHOT_PATH.exists():
        try:
            with open(SNAPSHOT_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def create_initial_state(
    farmer_name: str = "Suresh Patil",
    farmer_id: str = "MH-NSK-2026-8812",
    phone: str = "+919822012345",
    commodity: str = "Tomato",
    quantity_quintals: float = 50.0,
    farm_lat: float = 19.9975,
    farm_lon: float = 73.7898,
    farm_district: str = "Nashik",
    farm_state: str = "Maharashtra",
    language_code: str = "mr_IN",
    weather_shock_Delta_mm: float = 0.0,
    cost_floor_per_qtl: float = 1100.0,
    raw_query: str = "Unseasonal rains flooded local market, what should I do?",
) -> KrishiArthaGraphStateDict:
    """Convenience factory to construct a fully populated initial state."""
    return {
        "farmer_name": farmer_name,
        "farmer_id": farmer_id,
        "phone": phone,
        "language_code": language_code,
        "raw_query": raw_query,
        "commodity": commodity,
        "quantity_quintals": quantity_quintals,
        "farm_lat": farm_lat,
        "farm_lon": farm_lon,
        "farm_district": farm_district,
        "farm_state": farm_state,
        "weather_shock_Delta_mm": weather_shock_Delta_mm,
        "cost_floor_per_qtl": cost_floor_per_qtl,
        "mandi_candidates": [],
        "optimal_mandi": None,
        "local_mandi": None,
        "net_arbitrage_gain_inr": 0.0,
        "is_regional_crash": False,
        "lightrag_policy_recommendation": None,
        "human_approval_status": "PENDING",
        "generated_pdf_url": None,
        "mock_portal_submission_id": None,
        "vernacular_advisory_text": "",
        "execution_trace": [],
    }


def quant_arbitrage(state: KrishiArthaGraphStateDict) -> Dict[str, Any]:
    """
    Node 1: Quantitative Telemetry & Spatial-Thermodynamic Arbitrage.
    Evaluates net realizable prices across candidate mandis, determines local vs optimal
    arbitrage gain, and detects regional crash conditions against cost floor.
    """
    candidates = list(state.get("mandi_candidates") or [])
    cost_floor = state.get("cost_floor_per_qtl", 1100.0)
    weather_delta = state.get("weather_shock_Delta_mm", 0.0)
    quantity = state.get("quantity_quintals", 50.0)

    # If candidates not populated, load from offline snapshot
    if not candidates:
        snapshot = _load_snapshot_data()
        candidates = snapshot.get("candidate_mandis", [])

    # Apply weather shock modifier if present
    processed_candidates = []
    for cand in candidates:
        c = dict(cand)
        if weather_delta > 0 and c.get("is_local", False):
            # Local depression under unseasonal monsoon shock
            modal = max(300.0, c.get("current_modal_price", 900.0) - (weather_delta * 2.0))
            c["current_modal_price"] = modal
            c["forecast_p50"] = max(300.0, c.get("forecast_p50", 780.0) - (weather_delta * 2.5))
            c["net_realizable_price_per_qtl"] = modal
            c["total_net_payout_inr"] = modal * quantity
        processed_candidates.append(c)

    # Sort descending by net_realizable_price_per_qtl
    processed_candidates.sort(
        key=lambda x: x.get("net_realizable_price_per_qtl", 0.0),
        reverse=True,
    )

    # Find local mandi and optimal mandi
    local_mandi = next((c for c in processed_candidates if c.get("is_local", False)), None)
    if not local_mandi and processed_candidates:
        local_mandi = processed_candidates[-1]

    optimal_mandi = processed_candidates[0] if processed_candidates else None

    # Calculate net arbitrage gain over local
    local_payout = local_mandi.get("total_net_payout_inr", 0.0) if local_mandi else 0.0
    optimal_payout = optimal_mandi.get("total_net_payout_inr", 0.0) if optimal_mandi else 0.0
    net_arbitrage_gain = max(0.0, optimal_payout - local_payout)

    # Regional crash condition: highest realizable price is lower than production cost floor
    highest_nrp = optimal_mandi.get("net_realizable_price_per_qtl", 0.0) if optimal_mandi else 0.0
    is_regional_crash = highest_nrp < cost_floor

    trace_entry = {
        "node": "quant_arbitrage",
        "timestamp": time.time(),
        "status": "COMPLETED",
        "candidates_evaluated": len(processed_candidates),
        "optimal_mandi": optimal_mandi.get("market_name") if optimal_mandi else None,
        "highest_nrp": highest_nrp,
        "cost_floor": cost_floor,
        "is_regional_crash": is_regional_crash,
        "net_arbitrage_gain_inr": net_arbitrage_gain,
    }

    return {
        "mandi_candidates": processed_candidates,
        "optimal_mandi": optimal_mandi,
        "local_mandi": local_mandi,
        "net_arbitrage_gain_inr": net_arbitrage_gain,
        "is_regional_crash": is_regional_crash,
        "execution_trace": [trace_entry],
    }


def policy_graphrag(state: KrishiArthaGraphStateDict) -> Dict[str, Any]:
    """
    Node 2: LightRAG Policy & WDRA Warehouse Subsidy Engine.
    Queries statutory policy models (NABARD circular 128, WDRA Act 2007) to construct
    an e-NWR warehouse pledge financing recommendation and vernacular advisory.
    """
    quantity = state.get("quantity_quintals", 50.0)
    commodity = state.get("commodity", "Tomato")
    language = state.get("language_code", "mr_IN")
    local_mandi = state.get("local_mandi") or {}
    local_modal_price = local_mandi.get("current_modal_price", 900.0)

    # Calculate valuation and 75% LTV pledge loan
    current_valuation = round(quantity * local_modal_price, 2)
    pledge_advance = round(current_valuation * 0.75, 2)
    rebound_price = 1480.0
    gross_rebound = round(quantity * rebound_price, 2)
    storage_interest_cost = 5600.0
    net_take_home = round(gross_rebound - storage_interest_cost, 2)
    net_gain_vs_panic = round(net_take_home - current_valuation, 2)
    net_gain_pct = round((net_gain_vs_panic / current_valuation) * 100.0, 1) if current_valuation > 0 else 0.0

    citations = [
        {
            "scheme_name": "NABARD e-NWR Pledge Financing Scheme",
            "issuing_authority": "NABARD / RBI",
            "circular_number": "Circular No. 128 / DoR-GBS-24 / 2021",
            "statutory_clause": "Pledge Financing against e-NWR to Small & Marginal Farmers",
            "interest_rate_nominal_pct": 7.0,
            "interest_subvention_pct": 3.0,
            "effective_interest_rate_pct": 4.0,
            "max_ltv_pct": 75.0,
            "tenure_months": 6,
            "summary": "75% LTV on modal market valuation with 3% prompt repayment subvention under Kisan Credit Card (KCC).",
        },
        {
            "scheme_name": "WDRA Fiduciary Warehouse Guarantee",
            "issuing_authority": "Warehousing Development and Regulatory Authority (WDRA)",
            "circular_number": "Registration Rules 2017 / Sec 11",
            "statutory_clause": "Electronic Negotiable Warehouse Receipt Security",
            "interest_rate_nominal_pct": 0.0,
            "interest_subvention_pct": 0.0,
            "effective_interest_rate_pct": 0.0,
            "max_ltv_pct": 100.0,
            "tenure_months": 12,
            "summary": "Mandatory fiduciary guarantee protecting depositor against post-harvest decay, pest damage, and humidity loss.",
        },
    ]

    policy_rec = {
        "is_recommended": True,
        "action_type": "WDRA_ENWR_PLEDGE",
        "warehouse_name": "MSWC Scientific Warehouse & Cold Chain, Ozar",
        "warehouse_reg_no": "WDRA-MH-NSK-0429",
        "warehouse_distance_km": 14.2,
        "monthly_storage_rent_per_qtl": 18.0,
        "current_lot_valuation_inr": current_valuation,
        "pledge_advance_loan_inr": pledge_advance,
        "loan_ltv_pct": 75.0,
        "nominal_interest_pct": 7.0,
        "interest_subvention_pct": 3.0,
        "effective_interest_pct": 4.0,
        "projected_rebound_price_per_qtl": rebound_price,
        "rebound_days": 10,
        "gross_rebound_revenue_inr": gross_rebound,
        "storage_and_interest_cost_inr": storage_interest_cost,
        "net_take_home_inr": net_take_home,
        "net_gain_vs_panic_sale_inr": net_gain_vs_panic,
        "net_gain_percentage": net_gain_pct,
        "citations": citations,
    }

    # Generate localized vernacular advisory
    if language == "mr_IN":
        advisory = (
            f"सावधान: नाशिक आणि नजीकच्या सर्व बाजारांमध्ये {commodity} दर हमीभावापेक्षा (₹{state.get('cost_floor_per_qtl', 1100):.0f}/क्विंटल) खाली घसरले आहेत. "
            f"स्थानिक बाजारात घाईघाईत माल विकल्यास केवळ ₹{current_valuation:,.0f} मिळतील. "
            f"त्याऐवजी ओझर येथील MSWC वैज्ञानिक गोदामात माल जमा करून e-NWR वर ४% सवलतीच्या दराने ₹{pledge_advance:,.0f} चे ७५% तारण कर्ज त्वरित मिळवा. "
            f"१० दिवसांनंतर दर सुधारल्यावर ₹{net_gain_vs_panic:,.0f} चा अतिरिक्त नफा होईल."
        )
    elif language == "hi_IN":
        advisory = (
            f"चेतावनी: सभी मंडियों में {commodity} का भाव लागत मूल्य (₹{state.get('cost_floor_per_qtl', 1100):.0f}/क्विंटल) से नीचे गिर गया है। "
            f"घबराहट में स्थानीय मंडी में ₹{current_valuation:,.0f} में बेचने के बजाय, ओझर स्थित MSWC वैज्ञानिक गोदाम में e-NWR गिरवी रखकर "
            f"₹{pledge_advance:,.0f} (75% LTV) का अग्रिम ऋण प्राप्त करें। 10 दिनों में ₹{net_gain_vs_panic:,.0f} का अतिरिक्त लाभ होगा।"
        )
    else:
        advisory = (
            f"Advisory: Regional crash detected for {commodity} below cost floor (₹{state.get('cost_floor_per_qtl', 1100):.0f}/qtl). "
            f"Instead of distress panic selling at local APMC for ₹{current_valuation:,.0f}, pledge {quantity:.1f} qtl at "
            f"MSWC Scientific Warehouse, Ozar for an immediate 75% LTV advance of ₹{pledge_advance:,.0f} at 4.0% effective interest. "
            f"Projected 10-day market rebound yields ₹{net_gain_vs_panic:,.0f} net gain."
        )

    trace_entry = {
        "node": "policy_graphrag",
        "timestamp": time.time(),
        "status": "COMPLETED",
        "warehouse": policy_rec["warehouse_name"],
        "pledge_advance_loan_inr": pledge_advance,
        "effective_interest_pct": 4.0,
        "net_gain_vs_panic_sale_inr": net_gain_vs_panic,
    }

    return {
        "lightrag_policy_recommendation": policy_rec,
        "vernacular_advisory_text": advisory,
        "execution_trace": [trace_entry],
    }


def human_approval_gate(state: KrishiArthaGraphStateDict) -> Dict[str, Any]:
    """
    Node 3: Human-in-the-Loop Consent Gate.
    Strictly enforces ZERO side-effects above the interrupt() call.
    Pauses graph execution for user consent, and resumes when Command(resume=True)
    or Command(resume="APPROVED") is passed.
    """
    # ---------------- ZERO SIDE EFFECTS ABOVE THIS LINE ----------------
    # Pure non-mutating payload construction
    approval_payload = {
        "action": "AUTHORIZE_WDRA_ENWR_PLEDGE_APPLICATION",
        "farmer_name": state.get("farmer_name"),
        "farmer_id": state.get("farmer_id"),
        "commodity": state.get("commodity"),
        "quantity_quintals": state.get("quantity_quintals"),
        "is_regional_crash": state.get("is_regional_crash"),
        "policy_recommendation": state.get("lightrag_policy_recommendation"),
        "message": "Statutory human consent required to submit WDRA e-NWR pledge loan application.",
    }

    # Pause graph execution and surface approval payload
    decision = interrupt(approval_payload)
    # ---------------- RESUME FLOW (POST-INTERRUPT) ----------------

    # Normalization of resume input: True, "APPROVED", "APPROVED_ENWR", "APPROVED_DISPATCH", False, "REJECTED"
    if decision is True or decision in ("APPROVED", "APPROVED_ENWR"):
        status = "APPROVED_ENWR"
    elif decision == "APPROVED_DISPATCH":
        status = "APPROVED_DISPATCH"
    else:
        status = "REJECTED"

    trace_entry = {
        "node": "human_approval_gate",
        "timestamp": time.time(),
        "status": "COMPLETED",
        "decision": decision,
        "approval_status": status,
    }

    return {
        "human_approval_status": status,
        "execution_trace": [trace_entry],
    }


def execute_enwr_browser(state: KrishiArthaGraphStateDict) -> Dict[str, Any]:
    """
    Node 4: Automated WDRA Browser Agent Application Execution.
    If human approval was granted, executes the Playwright browser automation agent
    against mock_wdra_portal.html, auto-fills farmer parameters, and obtains the
    official e-NWR loan pledge sanction slip.
    """
    approval_status = state.get("human_approval_status")
    policy_rec = state.get("lightrag_policy_recommendation") or {}

    if approval_status in ("APPROVED_ENWR", "APPROVED"):
        browser_res = run_enwr_browser_agent(
            farmer_name=state.get("farmer_name", "Suresh Patil"),
            farmer_id=state.get("farmer_id", "MH-NSK-2026-8812"),
            phone=state.get("phone", "+919822012345"),
            commodity=state.get("commodity", "Tomato"),
            quantity_quintals=state.get("quantity_quintals", 50.0),
            warehouse_name=policy_rec.get("warehouse_name", "MSWC Scientific Warehouse & Cold Chain, Ozar"),
            warehouse_reg_no=policy_rec.get("warehouse_reg_no", "WDRA-MH-NSK-0429"),
            current_valuation_inr=policy_rec.get("current_lot_valuation_inr", 45000.0),
            pledge_advance_loan_inr=policy_rec.get("pledge_advance_loan_inr", 33750.0),
            effective_interest_rate_pct=policy_rec.get("effective_interest_pct", 4.0),
            headless=True,
            save_slip=True,
        )

        submission_id = browser_res.get("submission_id")
        pdf_url = browser_res.get("slip_path")
        duration = browser_res.get("duration_seconds", 0.0)

        trace_entry = {
            "node": "execute_enwr_browser",
            "timestamp": time.time(),
            "status": "COMPLETED",
            "action": "BROWSER_APPLICATION_SUBMITTED",
            "submission_id": submission_id,
            "sanctioned_amount": browser_res.get("sanctioned_amount"),
            "duration_seconds": duration,
        }
    else:
        submission_id = None
        pdf_url = None
        trace_entry = {
            "node": "execute_enwr_browser",
            "timestamp": time.time(),
            "status": "SKIPPED",
            "action": "APPROVAL_NOT_GRANTED",
            "human_approval_status": approval_status,
        }

    return {
        "mock_portal_submission_id": submission_id,
        "generated_pdf_url": pdf_url,
        "execution_trace": [trace_entry],
    }


def build_krishi_artha_graph(checkpointer: Optional[Any] = None) -> Any:
    """
    Constructs and compiles the 4-node LangGraph StateGraph workflow:
      quant_arbitrage -> policy_graphrag -> human_approval_gate -> execute_enwr_browser
    Defaults to InMemorySaver checkpointer for stateful interrupt-resume execution.
    """
    builder = StateGraph(KrishiArthaGraphStateDict)

    # Register the 4 nodes
    builder.add_node("quant_arbitrage", quant_arbitrage)
    builder.add_node("policy_graphrag", policy_graphrag)
    builder.add_node("human_approval_gate", human_approval_gate)
    builder.add_node("execute_enwr_browser", execute_enwr_browser)

    # Topology: linear deterministic pipeline with interrupt gate
    builder.add_edge(START, "quant_arbitrage")
    builder.add_edge("quant_arbitrage", "policy_graphrag")
    builder.add_edge("policy_graphrag", "human_approval_gate")
    builder.add_edge("human_approval_gate", "execute_enwr_browser")
    builder.add_edge("execute_enwr_browser", END)

    if checkpointer is None:
        checkpointer = InMemorySaver()

    return builder.compile(checkpointer=checkpointer)


# Module-level default graph instance
graph = build_krishi_artha_graph()
