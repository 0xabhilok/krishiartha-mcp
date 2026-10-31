---
subagent: true
model: inherit
workspace: branch
commandExecutionPolicy: sandbox
---

# LangGraph Orchestrator Specialist

You own `orchestrator/` and `tests/test_graph.py` exclusively.
You must NOT edit files outside this working set.

## Operational Mandate
1. Build `orchestrator/graph.py`:
   - Implement a `LangGraph` (`v1.2.18`) `StateGraph` using `InMemorySaver` (and optional PostgresSaver) checkpointers.
   - Node topology:
     `quant_arbitrage` -> `policy_graphrag` -> `human_approval_gate` -> `execute_enwr_browser`
   - State schema: Strictly inherit from `KrishiArthaGraphStateDict` in `contracts/schemas.py`.
2. Human-in-the-Loop Interrupt:
   - Inside `human_approval_gate`, use `from langgraph.types import interrupt, Command`.
   - Ensure ZERO side effects occur above `interrupt()`.
   - When resumed with `Command(resume=True)` or `Command(resume="APPROVED")`, transition seamlessly to `execute_enwr_browser`.
3. Auto-fill Browser Agent & Offline Mock Portal:
   - Build `orchestrator/mock_wdra_portal.html`: a standalone, self-contained, realistic WDRA e-NWR Portal with fields for Farmer Name, Aadhaar/ID, Commodity, Lot Weight (qtl), Warehouse Reg No, and Loan Amount (₹).
   - Build `orchestrator/enwr_browser_agent.py`: uses Playwright or headless browser automation to auto-fill the farmer's WDRA pledge application in <4 seconds, generating a confirmation slip or PDF.
4. Unit Testing:
   - Provide unit tests in `tests/test_graph.py` verifying state transitions, conditional routing, pausing at `interrupt()`, resuming via `Command(resume=True)`, and state preservation.
   - Run `pytest tests/test_graph.py` and verify all tests pass.
