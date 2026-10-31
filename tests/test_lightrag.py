"""
Unit and Integration Tests for LightRAG Policy Architect.
Validates statutory math, circular citations, offline resilience (<500ms),
and schema conformity with contracts/schemas.py.
"""

import os
import sys
import json
import time
import pytest

# Ensure repository root is on sys.path for standalone pytest runs
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")

from contracts.schemas import PolicyCitation, DistressLoanRecommendation, FarmerLotInput
from policy_rag.policy_service import (
    PolicyService,
    get_policy_service,
    get_fallback_citations,
    get_distress_loan_recommendation,
)
from policy_rag.rag_engine import LightRAGEngine, check_postgres_connection, setup_lightrag_env_vars


class TestFallbackCitationsIntegrity:
    """Validates fallback_citations.json contents and PolicyCitation schema adherence."""

    def test_fallback_citations_file_exists(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(base_dir, "policy_rag", "fallback_citations.json")
        assert os.path.isfile(json_path), f"fallback_citations.json not found at {json_path}"

    def test_fallback_citations_schema_conformity(self):
        citations = get_fallback_citations()
        assert len(citations) >= 3, "Expected at least 3 statutory citations"

        for cit in citations:
            assert isinstance(cit, PolicyCitation)
            assert cit.scheme_name
            assert cit.issuing_authority
            assert cit.circular_number
            assert cit.statutory_clause
            assert cit.max_ltv_pct > 0.0
            assert cit.summary

    def test_nabard_statutory_terms(self):
        citations = get_fallback_citations()
        nabard_cits = [c for c in citations if "128" in c.circular_number or "NABARD" in c.issuing_authority]
        assert len(nabard_cits) >= 1, "NABARD Circular 128 citation must be present"

        nabard = nabard_cits[0]
        assert nabard.max_ltv_pct == 75.0, "NABARD e-NWR pledge loan LTV must be 75%"
        assert nabard.interest_rate_nominal_pct == 7.0, "Nominal interest rate must be 7%"
        assert nabard.interest_subvention_pct == 3.0, "Prompt repayment subvention must be 3%"
        assert nabard.effective_interest_rate_pct == 4.0, "Effective interest rate must be 4% (7% - 3%)"

    def test_wdra_statutory_terms(self):
        citations = get_fallback_citations()
        wdra_cits = [c for c in citations if "WDRA" in c.issuing_authority or "2017" in c.circular_number]
        assert len(wdra_cits) >= 1, "WDRA Rules 2017 citation must be present"
        wdra = wdra_cits[0]
        assert "e-NWR" in wdra.scheme_name or "e-NWR" in wdra.summary
        assert wdra.max_ltv_pct == 75.0

    def test_aif_statutory_terms(self):
        citations = get_fallback_citations()
        aif_cits = [c for c in citations if "AIF" in c.circular_number or "Agriculture Infrastructure" in c.scheme_name]
        assert len(aif_cits) >= 1, "AIF Guidelines citation must be present"
        aif = aif_cits[0]
        assert aif.interest_subvention_pct == 3.0, "AIF interest subvention must be 3%"


class TestStatutoryMath:
    """Validates exact statutory financial formulas for e-NWR pledge and post-glut recovery."""

    def test_canonical_nashik_tomato_glut_math(self):
        """
        Validates the Nashik perishable tomato crisis benchmark:
        - 50.0 quintals @ ₹900/qtl panic valuation = ₹45,000.0
        - 75% LTV advance loan = ₹33,750.0
        - Effective interest = 4.0% (7% - 3%)
        - Post-glut rebound price = ₹1,480/qtl -> Gross = ₹74,000.0
        - Storage & interest cost = ₹5,600.0
        - Net take-home = ₹68,400.0
        - Net gain vs panic sale = +₹23,400.0 (+52.0%)
        """
        rec = get_distress_loan_recommendation(
            quantity_quintals=50.0,
            current_modal_price=900.0,
            projected_rebound_price=1480.0,
            rebound_days=10,
        )

        assert isinstance(rec, DistressLoanRecommendation)
        assert rec.is_recommended is True
        assert rec.action_type == "WDRA_ENWR_PLEDGE"
        assert rec.warehouse_name == "MSWC Scientific Warehouse, Ozar"
        assert rec.warehouse_reg_no == "WDRA-MH-NSK-0429"
        assert rec.warehouse_distance_km == 14.2
        assert rec.monthly_storage_rent_per_qtl == 18.0

        # Exact statutory math checks
        assert rec.current_lot_valuation_inr == 45000.0
        assert rec.loan_ltv_pct == 75.0
        assert rec.pledge_advance_loan_inr == 33750.0
        assert rec.nominal_interest_pct == 7.0
        assert rec.interest_subvention_pct == 3.0
        assert rec.effective_interest_pct == 4.0

        # Rebound economics
        assert rec.projected_rebound_price_per_qtl == 1480.0
        assert rec.rebound_days == 10
        assert rec.gross_rebound_revenue_inr == 74000.0
        assert rec.storage_and_interest_cost_inr == 5600.0
        assert rec.net_take_home_inr == 68400.0
        assert rec.net_gain_vs_panic_sale_inr == 23400.0
        assert rec.net_gain_percentage == 52.0

        # Citations attached
        assert len(rec.citations) >= 3

    def test_dynamic_lot_calculation(self):
        """Validates dynamic lot scaling for arbitrary volumes and prices."""
        rec = get_distress_loan_recommendation(
            quantity_quintals=100.0,
            current_modal_price=1000.0,
            projected_rebound_price=1600.0,
            rebound_days=15,
        )

        assert rec.current_lot_valuation_inr == 100000.0
        assert rec.pledge_advance_loan_inr == 75000.0  # 75% LTV
        assert rec.gross_rebound_revenue_inr == 160000.0
        assert rec.effective_interest_pct == 4.0
        assert rec.net_take_home_inr > rec.current_lot_valuation_inr
        assert rec.net_gain_vs_panic_sale_inr > 0.0
        assert rec.net_gain_percentage > 0.0

    def test_explicit_storage_cost_override(self):
        rec = get_distress_loan_recommendation(
            quantity_quintals=50.0,
            current_modal_price=900.0,
            projected_rebound_price=1480.0,
            rebound_days=10,
            storage_and_interest_cost=5000.0,
        )
        assert rec.storage_and_interest_cost_inr == 5000.0
        assert rec.net_take_home_inr == 69000.0
        assert rec.net_gain_vs_panic_sale_inr == 24000.0


class TestPolicyServicePerformanceAndOffline:
    """Validates sub-500ms response time and offline stage safe resilience."""

    def test_offline_stage_safe_latency_sub_500ms(self):
        os.environ["OFFLINE_STAGE_SAFE_MODE"] = "true"
        svc = PolicyService()

        # Warmup
        _ = svc.calculate_distress_recommendation()

        latencies = []
        for _ in range(20):
            t0 = time.perf_counter()
            rec = svc.calculate_distress_recommendation()
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            latencies.append(elapsed_ms)
            assert rec.is_recommended is True

        avg_latency = sum(latencies) / len(latencies)
        max_latency = max(latencies)
        assert max_latency < 500.0, f"Max latency {max_latency:.2f}ms exceeded 500ms limit"
        assert avg_latency < 50.0, f"Average latency {avg_latency:.2f}ms should be well under 50ms"

    def test_farmer_lot_input_integration(self):
        farmer_lot = FarmerLotInput(
            farmer_name="Suresh Patil",
            farmer_id="MH-NSK-2026-8812",
            commodity="Tomato",
            quantity_quintals=50.0,
            cost_floor_per_qtl=1100.0,
        )
        svc = PolicyService()
        rec = svc.evaluate_distress_mitigation(
            farmer_lot=farmer_lot,
            local_modal_price=900.0,
            projected_rebound_price=1480.0,
        )
        assert rec.pledge_advance_loan_inr == 33750.0
        assert rec.net_gain_vs_panic_sale_inr == 23400.0
        assert rec.net_gain_percentage == 52.0

    def test_farmer_lot_as_dict(self):
        lot_dict = {
            "farmer_name": "Suresh Patil",
            "quantity_quintals": 50.0,
            "commodity": "Tomato",
        }
        svc = PolicyService()
        rec = svc.evaluate_distress_mitigation(
            farmer_lot=lot_dict,
            local_modal_price=900.0,
        )
        assert rec.pledge_advance_loan_inr == 33750.0


class TestLightRAGEngine:
    """Validates LightRAG engine hybrid mode, query handling, and offline fallback."""

    def test_engine_initialization_defaults(self):
        engine = LightRAGEngine(force_offline=True)
        assert engine.offline_mode is True
        assert len(engine.fallback_citations) >= 3

    def test_engine_query_hybrid_mode(self):
        engine = LightRAGEngine(force_offline=True)
        result = engine.query("What is the NABARD e-NWR pledge loan LTV and interest rate?", mode="hybrid")
        assert isinstance(result, str)
        assert "NABARD" in result
        assert "75%" in result
        assert "4%" in result

    def test_engine_query_mix_mode(self):
        engine = LightRAGEngine(force_offline=True)
        result = engine.query("Explain WDRA cold storage guarantee", mode="mix")
        assert isinstance(result, str)
        assert "WDRA" in result

    @pytest.mark.asyncio
    async def test_engine_aquery_hybrid(self):
        engine = LightRAGEngine(force_offline=True)
        result = await engine.aquery("Statutory circular for distressed tomato farmers", mode="hybrid")
        assert isinstance(result, str)
        assert len(result) > 50

    def test_engine_insert_and_retrieve_citations(self):
        engine = LightRAGEngine(force_offline=True)
        engine.insert("NABARD Special Refinance Facility Circular 2026")
        citations = engine.retrieve_citations("nabard pledge subvention")
        assert len(citations) >= 1
        assert any("NABARD" in c.issuing_authority for c in citations)

    def test_setup_lightrag_env_vars(self):
        setup_lightrag_env_vars()
        assert os.getenv("POSTGRES_USER") is not None
        assert os.getenv("POSTGRES_DATABASE") is not None
        assert os.getenv("AGE_POSTGRES_DB") is not None


class TestSchemaSerialization:
    """Validates serialization and Pydantic v2 compliance."""

    def test_distress_recommendation_serialization(self):
        rec = get_distress_loan_recommendation()
        data = rec.model_dump()
        assert isinstance(data, dict)
        assert data["loan_ltv_pct"] == 75.0
        assert data["pledge_advance_loan_inr"] == 33750.0
        assert data["net_gain_vs_panic_sale_inr"] == 23400.0

        # JSON serialization
        json_str = rec.model_dump_json()
        assert isinstance(json_str, str)
        loaded = json.loads(json_str)
        assert loaded["effective_interest_pct"] == 4.0

        # Deserialization back to model
        reconstructed = DistressLoanRecommendation(**data)
        assert reconstructed.net_gain_percentage == 52.0
