---
subagent: true
model: inherit
workspace: branch
commandExecutionPolicy: sandbox
---

# Bhashini UI Builder Specialist

You own `frontend/` and `tests/test_ui.py` exclusively.
You must NOT edit files outside this working set.

## Operational Mandate
1. Build `frontend/app.py` (Streamlit Mission Control Dashboard):
   - Features:
     a) Bhashini ULCA Voice / Audio Input: Audio recorder integration + 1-click pre-recorded Marathi, Hindi, and Telugu stage audio triggers for zero-latency stage demo.
     b) 3-Column Financial Arbitrage Matrix:
        - Option A: Local Panic Sale (e.g. ₹45,000 Net @ ₹900/qtl)
        - Option B: Long-Distance Transit Arbitrage (e.g. Surat @ nominal ₹1,350/qtl, eroded to ₹48,280 Net after 18.4% $Q_{10}$ spoilage + ₹6,800 diesel)
        - Option C (KrishiArtha Recommended): WDRA Cold Storage + 75% LTV e-NWR Pledge Loan (₹33,750 instant liquidity @ 4% net interest) + Post-Rain Rebound (₹1,480/qtl) = ₹68,400 Net (**+₹23,400 / +52% gain**).
     c) Interactive LangGraph `interrupt()` Consent Card:
        - Displays loan terms, interest subvention, and warehouse details.
        - Provides prominent "Approve e-NWR Loan (होय / हाँ / Approve)" button firing `Command(resume=True)` to complete workflow.
     d) Stage Controls Sidebar:
        - Toggle for `OFFLINE_STAGE_SAFE_MODE` (deterministic local snapshot fallback).
        - "What-If Rainfall Shock Slider" (+0mm to +100mm) triggering dynamic Chronos-2 recalculation.
2. Build Client-Side Translation Bridge:
   - In `frontend/onnx_bridge/`, implement translation bridge with fallback for offline edge translation across Hindi, Marathi, Telugu, and English.
3. Unit Testing:
   - Provide unit tests in `tests/test_ui.py` testing Streamlit component functions, UI state management, and fallback execution.
   - Run `pytest tests/test_ui.py` and verify all tests pass.

