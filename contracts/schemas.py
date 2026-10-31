"""
KrishiArtha-MCP Contracts & Schema Registry
Defines frozen Pydantic v2 data models for interoperability between:
- FastMCP Quant Engine (mcp_server/)
- LightRAG Policy Architect (policy_rag/)
- LangGraph Orchestrator (orchestrator/)
- Bhashini UI Mission Control (frontend/)
"""

from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator
from pydantic import BaseModel, Field


class FarmerLotInput(BaseModel):
    """Farmer lot intake parameters."""
    farmer_name: str = Field(default="Suresh Patil", description="Name of farmer or FPO manager")
    farmer_id: Optional[str] = Field(default="MH-NSK-2026-8812", description="Aadhaar / FPO / KCC ID")
    phone: Optional[str] = Field(default="+919822012345", description="Contact phone number")
    commodity: str = Field(default="Tomato", description="Commodity name (e.g. Tomato, Onion)")
    variety: Optional[str] = Field(default="Deshi", description="Crop variety")
    quantity_quintals: float = Field(default=50.0, description="Lot volume in quintals (1 qtl = 100 kg)")
    farm_lat: float = Field(default=19.9975, description="Farm origin latitude")
    farm_lon: float = Field(default=73.7898, description="Farm origin longitude")
    farm_district: str = Field(default="Nashik", description="Farm district")
    farm_state: str = Field(default="Maharashtra", description="Farm state")
    language_code: str = Field(default="mr_IN", description="Language code: mr_IN, hi_IN, te_IN, en_IN")
    weather_shock_Delta_mm: float = Field(default=0.0, description="Interactive rainfall shock delta in mm")
    cost_floor_per_qtl: float = Field(default=1100.0, description="Minimum viable cost floor in INR/quintal")
    raw_query: Optional[str] = Field(default="", description="Original voice transcript or text query")


class MandiArbitrageOption(BaseModel):
    """Calculated metrics for a candidate APMC market."""
    market_name: str
    district: str
    state: str
    lat: float
    lon: float
    distance_km: float
    transit_hours: float
    current_modal_price: float
    forecast_p10: float
    forecast_p50: float
    forecast_p90: float
    spoilage_loss_pct: float
    spoilage_loss_quintals: float
    transport_cost_per_qtl: float
    total_transport_cost_inr: float
    mandi_fee_per_qtl: float
    net_realizable_price_per_qtl: float
    total_net_payout_inr: float
    arbitrage_gain_over_local_inr: float
    is_local: bool = False
    route_geojson: Optional[Dict[str, Any]] = None


class PolicyCitation(BaseModel):
    """Statutory policy citation from official circulars."""
    scheme_name: str
    issuing_authority: str
    circular_number: str
    statutory_clause: str
    interest_rate_nominal_pct: float
    interest_subvention_pct: float
    effective_interest_rate_pct: float
    max_ltv_pct: float
    tenure_months: int
    summary: str


class DistressLoanRecommendation(BaseModel):
    """WDRA e-NWR warehouse pledge loan & post-glut recovery recommendation."""
    is_recommended: bool = True
    action_type: str = "WDRA_ENWR_PLEDGE"
    warehouse_name: str = "MSWC Scientific Warehouse, Ozar"
    warehouse_reg_no: str = "WDRA-MH-NSK-0429"
    warehouse_distance_km: float = 14.2
    monthly_storage_rent_per_qtl: float = 18.0
    current_lot_valuation_inr: float = 45000.0
    pledge_advance_loan_inr: float = 33750.0  # 75% LTV
    loan_ltv_pct: float = 75.0
    nominal_interest_pct: float = 7.0
    interest_subvention_pct: float = 3.0
    effective_interest_pct: float = 4.0
    projected_rebound_price_per_qtl: float = 1480.0
    rebound_days: int = 10
    gross_rebound_revenue_inr: float = 74000.0
    storage_and_interest_cost_inr: float = 5600.0
    net_take_home_inr: float = 68400.0
    net_gain_vs_panic_sale_inr: float = 23400.0
    net_gain_percentage: float = 52.0
    citations: List[PolicyCitation] = []


class KrishiArthaGraphStateDict(TypedDict):
    """LangGraph v1.2.18 State Schema with Annotated trace reducers."""
    farmer_name: str
    farmer_id: str
    phone: str
    language_code: str
    raw_query: str
    commodity: str
    quantity_quintals: float
    farm_lat: float
    farm_lon: float
    farm_district: str
    farm_state: str
    weather_shock_Delta_mm: float
    cost_floor_per_qtl: float

    # Quantitative Telemetry & Forecasts
    mandi_candidates: List[Dict[str, Any]]
    optimal_mandi: Optional[Dict[str, Any]]
    local_mandi: Optional[Dict[str, Any]]
    net_arbitrage_gain_inr: float
    is_regional_crash: bool

    # Policy & e-NWR Recommendation
    lightrag_policy_recommendation: Optional[Dict[str, Any]]

    # Human-in-the-Loop & Statutory Action
    human_approval_status: Optional[str]  # "PENDING", "APPROVED_DISPATCH", "APPROVED_ENWR", "REJECTED"
    generated_pdf_url: Optional[str]
    mock_portal_submission_id: Optional[str]
    vernacular_advisory_text: str

    # Reducer accumulator for live tracing
    execution_trace: Annotated[List[Dict[str, Any]], operator.add]

