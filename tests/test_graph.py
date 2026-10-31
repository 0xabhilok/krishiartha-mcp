"""
Unit and Integration Tests for KrishiArtha-MCP LangGraph Orchestrator & WDRA Browser Agent.
Validates:
  1. Quant Arbitrage node calculations & regional crash detection.
  2. Policy GraphRAG node recommendations & vernacular advisory generation.
  3. enwr_browser_agent automated form submission in <4 seconds.
  4. LangGraph 4-node topology state transitions.
  5. Pausing at human_approval_gate interrupt().
  6. Resuming via Command(resume=True) and Command(resume="APPROVED").
  7. Rejection handling via Command(resume=False).
"""

import uuid
import time
import pytest
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver

from contracts.schemas import KrishiArthaGraphStateDict
from orchestrator.graph import (
    build_krishi_artha_graph,
    create_initial_state,
    quant_arbitrage,
    policy_graphrag,
    human_approval_gate,
    execute_enwr_browser,
)
from orchestrator.enwr_browser_agent import run_enwr_browser_agent


class TestQuantArbitrageNode:
    """Tests for Node 1: quant_arbitrage."""

    def test_regional_crash_detection(self):
        state = create_initial_state(cost_floor_per_qtl=1100.0)
        res = quant_arbitrage(state)

        assert "optimal_mandi" in res
        assert "local_mandi" in res
        assert res["is_regional_crash"] is True
        assert res["optimal_mandi"]["net_realizable_price_per_qtl"] < 1100.0
        assert len(res["execution_trace"]) == 1
        assert res["execution_trace"][0]["node"] == "quant_arbitrage"

    def test_profitable_arbitrage_no_crash(self):
        state = create_initial_state(cost_floor_per_qtl=800.0)
        res = quant_arbitrage(state)

        assert res["is_regional_crash"] is False
        assert res["optimal_mandi"]["net_realizable_price_per_qtl"] >= 800.0

    def test_weather_shock_impact(self):
        state_dry = create_initial_state(weather_shock_Delta_mm=0.0)
        res_dry = quant_arbitrage(state_dry)

        state_shock = create_initial_state(weather_shock_Delta_mm=40.0)
        res_shock = quant_arbitrage(state_shock)

        local_dry_price = res_dry["local_mandi"]["current_modal_price"]
        local_shock_price = res_shock["local_mandi"]["current_modal_price"]
        assert local_shock_price < local_dry_price


class TestPolicyGraphRAGNode:
    """Tests for Node 2: policy_graphrag."""

    def test_policy_recommendation_and_citations(self):
        state = create_initial_state()
        state.update(quant_arbitrage(state))

        res = policy_graphrag(state)
        rec = res["lightrag_policy_recommendation"]

        assert rec["is_recommended"] is True
        assert rec["action_type"] == "WDRA_ENWR_PLEDGE"
        assert rec["warehouse_reg_no"] == "WDRA-MH-NSK-0429"
        assert rec["loan_ltv_pct"] == 75.0
        assert rec["effective_interest_pct"] == 4.0
        assert rec["pledge_advance_loan_inr"] == 33750.0  # 45000 * 0.75
        assert len(rec["citations"]) >= 2
        assert any("128" in c["circular_number"] for c in rec["citations"])
        assert len(res["execution_trace"]) == 1

    def test_multilingual_vernacular_advisories(self):
        for lang in ["mr_IN", "hi_IN", "en_IN"]:
            state = create_initial_state(language_code=lang)
            state.update(quant_arbitrage(state))
            res = policy_graphrag(state)
            advisory = res["vernacular_advisory_text"]
            assert len(advisory) > 20
            if lang == "mr_IN":
                assert "सावधान" in advisory or "गोदामात" in advisory
            elif lang == "hi_IN":
                assert "चेतावनी" in advisory or "गोदाम" in advisory


class TestENWRBrowserAgent:
    """Tests for Auto-fill Browser Agent & Mock Portal."""

    def test_automated_fill_under_four_seconds(self):
        t0 = time.time()
        result = run_enwr_browser_agent(
            farmer_name="Suresh Patil",
            farmer_id="MH-NSK-2026-8812",
            commodity="Tomato",
            quantity_quintals=50.0,
            pledge_advance_loan_inr=33750.0,
            headless=True,
            save_slip=True,
        )
        elapsed = time.time() - t0

        assert result["success"] is True
        assert "WDRA-ENWR" in result["submission_id"]
        assert "SANCTIONED" in result["status"]
        assert result["quantity_quintals"] == 50.0
        assert result["duration_seconds"] < 4.0
        assert elapsed < 4.0


class TestLangGraphStateTransitionsAndInterrupt:
    """Tests for LangGraph StateGraph execution, interrupt gate, and resumes."""

    def test_graph_pauses_at_human_approval_interrupt(self):
        graph = build_krishi_artha_graph()
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}

        initial_state = create_initial_state()
        result = graph.invoke(initial_state, config=config)

        # Execution must pause at human_approval_gate
        assert "__interrupt__" in result
        interrupt_list = result["__interrupt__"]
        assert len(interrupt_list) == 1

        interrupt_payload = interrupt_list[0].value
        assert interrupt_payload["action"] == "AUTHORIZE_WDRA_ENWR_PLEDGE_APPLICATION"
        assert interrupt_payload["farmer_name"] == "Suresh Patil"
        assert interrupt_payload["quantity_quintals"] == 50.0
        assert interrupt_payload["policy_recommendation"]["pledge_advance_loan_inr"] == 33750.0

        # Verify graph checkpoint state
        snapshot = graph.get_state(config)
        assert snapshot.next == ("human_approval_gate",)
        assert snapshot.values["is_regional_crash"] is True
        assert snapshot.values["optimal_mandi"] is not None

    def test_resume_via_command_resume_true(self):
        graph = build_krishi_artha_graph()
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}

        # Pause at gate
        graph.invoke(create_initial_state(), config=config)

        # Resume with Command(resume=True)
        final_state = graph.invoke(Command(resume=True), config=config)

        assert final_state["human_approval_status"] == "APPROVED_ENWR"
        assert final_state["mock_portal_submission_id"] is not None
        assert "WDRA-ENWR" in final_state["mock_portal_submission_id"]
        assert final_state["generated_pdf_url"] is not None

        # Verify all 4 nodes executed in trace
        nodes = [t["node"] for t in final_state["execution_trace"]]
        assert nodes == ["quant_arbitrage", "policy_graphrag", "human_approval_gate", "execute_enwr_browser"]

    def test_resume_via_command_resume_approved_string(self):
        graph = build_krishi_artha_graph()
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}

        # Pause at gate
        graph.invoke(create_initial_state(), config=config)

        # Resume with Command(resume="APPROVED")
        final_state = graph.invoke(Command(resume="APPROVED"), config=config)

        assert final_state["human_approval_status"] == "APPROVED_ENWR"
        assert final_state["mock_portal_submission_id"] is not None
        assert "WDRA-ENWR" in final_state["mock_portal_submission_id"]

    def test_resume_via_command_resume_rejected(self):
        graph = build_krishi_artha_graph()
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}

        # Pause at gate
        graph.invoke(create_initial_state(), config=config)

        # Resume with Command(resume=False)
        final_state = graph.invoke(Command(resume=False), config=config)

        assert final_state["human_approval_status"] == "REJECTED"
        assert final_state["mock_portal_submission_id"] is None
        assert final_state["generated_pdf_url"] is None

        # Verify browser node marked skipped in trace
        nodes = [t["node"] for t in final_state["execution_trace"]]
        assert "execute_enwr_browser" in nodes
        last_trace = final_state["execution_trace"][-1]
        assert last_trace["status"] == "SKIPPED"
        assert last_trace["action"] == "APPROVAL_NOT_GRANTED"
