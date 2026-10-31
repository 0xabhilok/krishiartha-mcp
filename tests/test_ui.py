"""
KrishiArtha-MCP: Bhashini UI Mission Control Unit Tests
Tests dashboard logic, financial arbitrage calculations, Q10 spoilage deductions,
offline translation bridge across Marathi, Hindi, Telugu, English,
interactive LangGraph interrupt consent handling, and Streamlit AppTest execution.
"""

import pytest
import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from frontend.onnx_bridge.translator import (
    OfflineTranslator,
    get_translator,
    translate_text,
    SUPPORTED_LANGUAGES,
    STAGE_AUDIO_PROMPTS,
    VERNACULAR_ADVISORY,
)
from frontend.arbitrage_engine import (
    compute_arbitrage_matrix,
    execute_langgraph_consent,
    load_offline_snapshot,
)
from contracts.schemas import (
    FarmerLotInput,
    MandiArbitrageOption,
    DistressLoanRecommendation,
    PolicyCitation,
    KrishiArthaGraphStateDict,
)


class TestTranslationBridge:
    """Tests for offline edge translation across scheduled Indian languages."""

    def test_supported_languages(self):
        translator = get_translator()
        langs = translator.get_supported_languages()
        assert "mr" in langs
        assert "hi" in langs
        assert "te" in langs
        assert "en" in langs

    def test_language_code_normalization(self):
        translator = get_translator()
        assert translator.normalize_lang_code("mr_IN") == "mr"
        assert translator.normalize_lang_code("hi_IN") == "hi"
        assert translator.normalize_lang_code("te_IN") == "te"
        assert translator.normalize_lang_code("en_IN") == "en"
        assert translator.normalize_lang_code("Marathi") == "mr"
        assert translator.normalize_lang_code("Hindi") == "hi"
        assert translator.normalize_lang_code("Telugu") == "te"
        assert translator.normalize_lang_code("English") == "en"

    def test_marathi_translations(self):
        translator = get_translator()
        assert "स्थानिक" in translator.translate("Option A: Local Panic Sale", "mr")
        assert "सुरत" in translator.translate("Option B: Surat Transit Arbitrage", "mr")
        assert "शीतगृह" in translator.translate("Option C: WDRA Cold Storage + e-NWR Loan", "mr")
        assert "मंजूर" in translator.translate("Approve e-NWR Loan (Approve)", "mr")

    def test_hindi_translations(self):
        translator = get_translator()
        assert "स्थानीय" in translator.translate("Option A: Local Panic Sale", "hi")
        assert "सूरत" in translator.translate("Option B: Surat Transit Arbitrage", "hi")
        assert "कोल्ड स्टोरेज" in translator.translate("Option C: WDRA Cold Storage + e-NWR Loan", "hi")
        assert "स्वीकृत" in translator.translate("Approve e-NWR Loan (Approve)", "hi")

    def test_telugu_translations(self):
        translator = get_translator()
        assert "స్థానిక" in translator.translate("Option A: Local Panic Sale", "te")
        assert "సూరత్" in translator.translate("Option B: Surat Transit Arbitrage", "te")
        assert "శీతల నిల్వ" in translator.translate("Option C: WDRA Cold Storage + e-NWR Loan", "te")
        assert "ఆమోదించు" in translator.translate("Approve e-NWR Loan (Approve)", "te")

    def test_stage_demo_prompts(self):
        translator = get_translator()
        for code in ["mr", "hi", "te", "en"]:
            prompt = translator.get_stage_prompt(code)
            assert len(prompt) > 20
            assert "५०" in prompt or "50" in prompt

    def test_vernacular_advisories(self):
        translator = get_translator()
        for code in ["mr", "hi", "te", "en"]:
            advisory = translator.get_vernacular_advisory(code)
            assert len(advisory) > 50
            assert "68,400" in advisory or "६८,४००" in advisory or "68400" in advisory

    def test_offline_readiness_and_fallback(self):
        translator = get_translator()
        assert translator.is_offline_ready() is True
        # Unknown phrase fallback returns original text
        unknown = "Unseen Agricultural Phrase 12345"
        assert translator.translate(unknown, "mr") == unknown


class TestFinancialArbitrageMatrix:
    """Tests exact financial matrix calculations, Q10 spoilage, and distress protocols."""

    def test_canonical_zero_shock_matrix(self):
        """Validates canonical baseline figures when rainfall shock = 0mm."""
        matrix = compute_arbitrage_matrix(quantity_qtl=50.0, rainfall_shock_mm=0.0)

        # Option A: Local Panic Sale
        opt_a = matrix["option_a"]
        assert opt_a["total_net_payout_inr"] == 45000.0
        assert opt_a["modal_price_per_qtl"] == 900.0
        assert opt_a["net_realizable_price_per_qtl"] == 900.0
        assert opt_a["loss_vs_cost_floor_inr"] == 10000.0  # (1100 - 900) * 50

        # Option B: Surat Transit Arbitrage
        opt_b = matrix["option_b"]
        assert opt_b["nominal_modal_price_per_qtl"] == 1350.0
        assert opt_b["spoilage_loss_pct"] == 18.4
        assert opt_b["spoilage_loss_quintals"] == 9.2
        assert opt_b["transport_cost_inr"] == 6800.0
        assert opt_b["total_net_payout_inr"] == 48280.0
        assert opt_b["net_realizable_price_per_qtl"] == 965.6
        assert opt_b["arbitrage_gain_over_local_inr"] == 3280.0

        # Option C: WDRA Cold Storage + 75% e-NWR Loan (Recommended)
        opt_c = matrix["option_c"]
        assert opt_c["current_lot_valuation_inr"] == 45000.0
        assert opt_c["pledge_advance_loan_inr"] == 33750.0  # 75% LTV
        assert opt_c["effective_interest_pct"] == 4.0  # 7% - 3% KCC subvention
        assert opt_c["gross_rebound_revenue_inr"] == 74000.0
        assert opt_c["storage_and_interest_cost_inr"] == 5600.0
        assert opt_c["net_take_home_inr"] == 68400.0
        assert opt_c["net_gain_vs_local_inr"] == 23400.0
        assert opt_c["net_gain_percentage"] == 52.0

        # Regional Crash Flag
        assert matrix["is_regional_crash"] is True

    def test_cost_floor_breach(self):
        """Verifies both local and transit mandis fall below cost floor of ₹1100/qtl."""
        matrix = compute_arbitrage_matrix(quantity_qtl=50.0, rainfall_shock_mm=0.0, cost_floor_per_qtl=1100.0)
        assert matrix["option_a"]["net_realizable_price_per_qtl"] < 1100.0
        assert matrix["option_b"]["net_realizable_price_per_qtl"] < 1100.0
        assert matrix["is_regional_crash"] is True

    def test_what_if_rainfall_shock_dynamics(self):
        """Tests that unseasonal rain shock (+45mm) triggers expected physical & economic shifts."""
        base_matrix = compute_arbitrage_matrix(quantity_qtl=50.0, rainfall_shock_mm=0.0)
        shocked_matrix = compute_arbitrage_matrix(quantity_qtl=50.0, rainfall_shock_mm=45.0)

        # 1. Local panic price decreases under shock
        assert (
            shocked_matrix["option_a"]["total_net_payout_inr"]
            < base_matrix["option_a"]["total_net_payout_inr"]
        )

        # 2. Surat transit spoilage and transport costs escalate
        assert (
            shocked_matrix["option_b"]["spoilage_loss_pct"]
            > base_matrix["option_b"]["spoilage_loss_pct"]
        )
        assert (
            shocked_matrix["option_b"]["transport_cost_inr"]
            > base_matrix["option_b"]["transport_cost_inr"]
        )

        # 3. Option C rebound price increases due to field destruction scarcity
        assert (
            shocked_matrix["option_c"]["projected_rebound_price_per_qtl"]
            > base_matrix["option_c"]["projected_rebound_price_per_qtl"]
        )

        # 4. Net advantage of storage widens under extreme shock
        assert (
            shocked_matrix["option_c"]["net_gain_vs_local_inr"]
            > base_matrix["option_c"]["net_gain_vs_local_inr"]
        )


class TestLangGraphConsentCard:
    """Tests LangGraph interrupt() approval and resume flow."""

    def test_approve_enwr_loan(self):
        res = execute_langgraph_consent(
            action="APPROVE",
            farmer_name="Suresh Patil",
            farmer_id="MH-NSK-2026-8812",
            commodity="Tomato",
            quantity_qtl=50.0,
            loan_amount=33750.0,
            warehouse_reg_no="WDRA-MH-NSK-0429",
        )
        assert res["status"] == "APPROVED_ENWR"
        assert res["action"] == "Command(resume=True)"
        assert res["pledge_loan_amount_inr"] == 33750.0
        assert res["submission_id"].startswith("WDRA-ENWR-2026-")
        assert "GP-0429-" in res["gate_pass_code"]

    def test_reject_local_sale(self):
        res = execute_langgraph_consent(
            action="REJECT",
            farmer_name="Suresh Patil",
            farmer_id="MH-NSK-2026-8812",
            commodity="Tomato",
            quantity_qtl=50.0,
            loan_amount=33750.0,
            warehouse_reg_no="WDRA-MH-NSK-0429",
        )
        assert res["status"] == "REJECTED_LOCAL_SALE"
        assert res["action"] == "Command(resume=False)"
        assert res["pledge_loan_amount_inr"] == 0.0


class TestOfflineSnapshotLoading:
    """Tests offline dataset loading for zero-latency stage demo."""

    def test_load_snapshot_structure(self):
        snapshot = load_offline_snapshot()
        assert "farmer_lot" in snapshot
        assert "candidate_mandis" in snapshot
        assert "recommended_distress_solution" in snapshot
        assert snapshot["farmer_lot"]["farmer_name"] == "Suresh Patil"
        assert snapshot["farmer_lot"]["quantity_quintals"] == 50.0


class TestSchemaContractsInteroperability:
    """Validates data structures match frozen Pydantic contracts in contracts/schemas.py."""

    def test_distress_loan_schema_compatibility(self):
        matrix = compute_arbitrage_matrix()
        opt_c = matrix["option_c"]

        rec = DistressLoanRecommendation(
            is_recommended=True,
            action_type="WDRA_ENWR_PLEDGE",
            warehouse_name=opt_c["warehouse_name"],
            warehouse_reg_no=opt_c["warehouse_reg_no"],
            warehouse_distance_km=opt_c["distance_km"],
            monthly_storage_rent_per_qtl=18.0,
            current_lot_valuation_inr=opt_c["current_lot_valuation_inr"],
            pledge_advance_loan_inr=opt_c["pledge_advance_loan_inr"],
            loan_ltv_pct=opt_c["loan_ltv_pct"],
            nominal_interest_pct=opt_c["nominal_interest_pct"],
            interest_subvention_pct=opt_c["interest_subvention_pct"],
            effective_interest_pct=opt_c["effective_interest_pct"],
            projected_rebound_price_per_qtl=opt_c["projected_rebound_price_per_qtl"],
            rebound_days=opt_c["rebound_days"],
            gross_rebound_revenue_inr=opt_c["gross_rebound_revenue_inr"],
            storage_and_interest_cost_inr=opt_c["storage_and_interest_cost_inr"],
            net_take_home_inr=opt_c["net_take_home_inr"],
            net_gain_vs_panic_sale_inr=opt_c["net_gain_vs_local_inr"],
            net_gain_percentage=opt_c["net_gain_percentage"],
            citations=[],
        )
        assert rec.pledge_advance_loan_inr == 33750.0
        assert rec.net_take_home_inr == 68400.0
        assert rec.net_gain_vs_panic_sale_inr == 23400.0

    def test_mandi_arbitrage_schema_compatibility(self):
        matrix = compute_arbitrage_matrix()
        opt_b = matrix["option_b"]

        mandi_opt = MandiArbitrageOption(
            market_name=opt_b["market_name"],
            district="Surat",
            state="Gujarat",
            lat=21.1702,
            lon=72.8311,
            distance_km=234.0,
            transit_hours=5.2,
            current_modal_price=opt_b["nominal_modal_price_per_qtl"],
            forecast_p10=1150.0,
            forecast_p50=1340.0,
            forecast_p90=1490.0,
            spoilage_loss_pct=opt_b["spoilage_loss_pct"],
            spoilage_loss_quintals=opt_b["spoilage_loss_quintals"],
            transport_cost_per_qtl=136.0,
            total_transport_cost_inr=opt_b["transport_cost_inr"],
            mandi_fee_per_qtl=20.25,
            net_realizable_price_per_qtl=opt_b["net_realizable_price_per_qtl"],
            total_net_payout_inr=opt_b["total_net_payout_inr"],
            arbitrage_gain_over_local_inr=opt_b["arbitrage_gain_over_local_inr"],
            is_local=False,
        )
        assert mandi_opt.total_net_payout_inr == 48280.0
        assert mandi_opt.spoilage_loss_pct == 18.4


class TestStreamlitAppExecution:
    """Verifies that the Streamlit app loads and executes without errors via AppTest."""

    def test_streamlit_apptest_run(self):
        from streamlit.testing.v1 import AppTest

        app_path = str(Path(__file__).resolve().parent.parent / "frontend" / "app.py")
        at = AppTest.from_file(app_path)
        at.run()

        assert not at.exception, f"App execution raised exception: {at.exception}"
        # Check sidebar elements exist
        assert len(at.sidebar.toggle) > 0
        assert len(at.sidebar.slider) > 0
        # Check title renders
        assert any("KrishiArtha-MCP" in str(title.value) for title in at.title)

    def test_streamlit_language_switching(self):
        from streamlit.testing.v1 import AppTest

        app_path = str(Path(__file__).resolve().parent.parent / "frontend" / "app.py")
        at = AppTest.from_file(app_path)
        at.run()

        # Switch to Hindi
        at.sidebar.selectbox[0].select("hi").run()
        assert not at.exception
        assert at.session_state.selected_language == "hi"

        # Switch to Telugu
        at.sidebar.selectbox[0].select("te").run()
        assert not at.exception
        assert at.session_state.selected_language == "te"

        # Switch to English
        at.sidebar.selectbox[0].select("en").run()
        assert not at.exception
        assert at.session_state.selected_language == "en"

    def test_streamlit_approval_button_click(self):
        from streamlit.testing.v1 import AppTest

        app_path = str(Path(__file__).resolve().parent.parent / "frontend" / "app.py")
        at = AppTest.from_file(app_path)
        at.run()

        # Find and click the Approve button
        approve_buttons = [btn for btn in at.button if "Approve" in btn.label or "मंजूर" in btn.label]
        assert len(approve_buttons) > 0, "Approve button not found in app"
        approve_buttons[0].click().run()

        assert not at.exception
        assert at.session_state.approval_status == "APPROVED_ENWR"
        assert at.session_state.approval_result is not None
        assert at.session_state.approval_result["action"] == "Command(resume=True)"
