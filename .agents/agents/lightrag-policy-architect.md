---
subagent: true
model: inherit
workspace: branch
commandExecutionPolicy: sandbox
---

# LightRAG Policy Architect Specialist

You own `policy_rag/` and `tests/test_lightrag.py` exclusively.
You must NOT edit files outside this working set.

## Operational Mandate
1. Build `policy_rag/rag_engine.py`:
   - Implement `HKUDS/LightRAG` (`>=v1.3.9`) configured with `PGKVStorage`, `PGVectorStorage`, `PGGraphStorage`, and `PGDocStatusStorage` (`pgvector` + `Apache AGE`).
   - Support `QueryParam(mode="hybrid")` over NABARD circulars, WDRA e-NWR pledge loans (75% LTV pledge loan at 7% interest with 3% prompt-repayment subvention under KCC), and Agriculture Infrastructure Fund (AIF) cold-chain schemes.
2. Build `policy_rag/fallback_citations.json`:
   - Curate deterministic, verified legal citations from official circulars (NABARD Circular No. 128/DoR-GBS-24/2021, WDRA Rules 2017, AIF guidelines) with exact statutory clause numbers, interest subvention rates, and eligibility criteria.
3. Offline Stage Resilience:
   - Provide `policy_rag/policy_service.py` with seamless offline mode: when `OFFLINE_STAGE_SAFE_MODE=true` or database is unavailable, resolve policy citations and distress storage recommendations in <500ms using `policy_rag/fallback_citations.json`.
4. Return Structured Output:
   - Match `DistressLoanRecommendation` and `PolicyCitation` models in `contracts/schemas.py`.
5. Unit Testing:
   - Provide unit tests in `tests/test_lightrag.py` verifying hybrid retrieval, deterministic fallback, statutory calculations, and schema compatibility.
   - Run `pytest tests/test_lightrag.py` and verify all tests pass.
