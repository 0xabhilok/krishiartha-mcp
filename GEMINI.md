# PROJECT: KrishiArtha-MCP (MandiPulse) — Autonomous Covariate Mandi Arbitrage & Policy Execution Engine
# ARCHITECTURE: KrishiArtha-MCP — Production Specification
# AUTHOR: Abhilok Reddy
# DOMAIN: Climate & Supply Resilience + Civic Pulse & Digital Public Infrastructure (DPI)

## 1. CORE ARCHITECTURAL MANDATE
KrishiArtha-MCP is a production-grade, neuro-symbolic multi-agent agricultural supply-chain and spatial arbitrage engine.
- **No LLM Math Hallucinations:** Never ask an LLM to guess future commodity prices, road distances, or spoilage percentages.
- **Deterministic & Foundation Model Spine:**
  1. **Time-Series Forecasting:** `amazon/chronos-2` (or `autogluon/chronos-2-small`) using historical wholesale prices + 7-day Open-Meteo rainfall/temperature exogenous covariates outputting $P_{10}, P_{50}, P_{90}$ quantiles.
  2. **Spatial-Thermodynamic Arbitrage:** Deterministic physics & economics using OSRM highway distances (`router.project-osrm.org`), round-trip diesel freight ($2 \cdot d_{\text{km}} \cdot ₹22/\text{km} + Q \cdot ₹35/\text{qtl}$ loading), Arrhenius $Q_{10}$ thermal-humidity transit decay with mandatory +2.5h APMC queue buffer, and state APMC market fee deductions.
  3. **Policy & Subsidy Reasoning:** `HKUDS/LightRAG` (>= v1.3.9) in `mix` mode over NABARD Circular 128 (75% LTV, 7% base with 3% prompt repayment subvention = 4% net interest under KCC) and WDRA warehouse guarantees.
  4. **Orchestration:** `langchain-ai/langgraph` (v1.2.18) `StateGraph` with `InMemorySaver` checkpointer and an explicit `interrupt()` human-in-the-loop gate before statutory PDF generation or truck dispatch.
  5. **Data Ingestion:** Standardized Model Context Protocol (`FastMCP`) tool servers wrapping `mandi-api.onrender.com/v1/prices`, `api.data.gov.in` (OGD resource IDs `9ef84268-d588-465a-a308-a864a43d0070` and `35985678-0d79-46b4-9ed6-6f13308a1d24`), and Open-Meteo.
  6. **Multilingual Voice & Vernacular Edge:** Bhashini ULCA ASR/TTS across 22 scheduled Indian languages paired with client-side translation bridge for Marathi, Hindi, Telugu, and English.
  7. **Offline Evaluation Resilience:** Every component obeys `OFFLINE_STAGE_SAFE_MODE=true` (or >2.5s network timeout fallback) reading deterministic local snapshots from `data/offline_snapshots/nashik_tomato_glut.json`.

---

## 2. DIRECTORY STRUCTURE
```plaintext
krishiartha-mcp/
├── contracts/
│   └── schemas.py              # Frozen Pydantic v2 schemas
├── mcp_server/
│   ├── server.py               # FastMCP server (mandi, weather, routing tools)
│   ├── chronos_engine.py       # Chronos-2 weather-covariate quantile forecaster
│   └── spoilage_arbitrage.py   # Arrhenius Q10 decay + OSRM diesel transport math
├── policy_rag/
│   ├── rag_engine.py           # LightRAG hybrid knowledge graph engine
│   ├── policy_service.py       # Statutory loan recommendation service (<500ms SLA)
│   └── fallback_citations.json # Deterministic NABARD/WDRA/AIF statutory clauses
├── orchestrator/
│   ├── graph.py                # 4-node LangGraph StateGraph with interrupt() gate
│   ├── enwr_browser_agent.py   # Automated WDRA portal form filler (<1.5s SLA)
│   └── mock_wdra_portal.html   # Standalone HTML WDRA e-NWR portal
├── frontend/
│   ├── app.py                  # Streamlit Mission Control Cockpit
│   ├── arbitrage_engine.py     # 3-column financial matrix & rainfall shock simulator
│   └── onnx_bridge/translator.py # Multilingual Indic translation bridge
├── data/
│   └── offline_snapshots/
│       └── nashik_tomato_glut.json # Canonical 50qtl Nashik tomato glut dataset
├── tests/
│   ├── test_quant.py           # 23 FastMCP & Quant math tests (100% pass)
│   ├── test_lightrag.py        # 18 LightRAG & statutory policy tests (100% pass)
│   ├── test_graph.py           # 10 LangGraph state machine & interrupt tests (100% pass)
│   └── test_ui.py              # 19 Streamlit UI & translation tests (100% pass)
├── docker-compose.yml          # Container stack (Postgres/AGE/pgvector + FastAPI + UI)
├── requirements.txt            # Python dependencies
└── pytest.ini                  # Pytest configuration
```

---

## 3. SCIENTIFIC & MATHEMATICAL FORMULAS

### A. Arrhenius Q10 Biological Spoilage Decay
$$k(T_{\text{amb}}, RH) = k_{\text{base}} \cdot \left(Q_{10}\right)^{\frac{T_{\text{amb}} - 20.0}{10.0}} \cdot \left(1 + \alpha_{\text{hum}} \cdot \max\left(0, \frac{RH - 70}{100}\right)\right)$$
- Baseline rate at 20°C: $k_{\text{base}} = 0.0065$ (Tomato), $0.0018$ (Onion), $0.0050$ (Greens).
- Moisture rot multiplier: $\alpha_{\text{hum}} = 1.5$.
- Temperature coefficient: $Q_{10} = 2.2$.
- Transit duration buffer: $t_{\text{transit}} = t_{\text{duration}} + 2.5\text{h}$ unloading queue.
- Spoilage loss fraction: $L = 1 - \exp\left(-k \cdot t_{\text{transit}}\right)$.

### B. Freight & Handling Deductions
$$C_{\text{transport}} = 2 \cdot d_{\text{km}} \cdot r_{\text{diesel\_per\_km}} + Q \cdot C_{\text{loading\_per\_qtl}}$$
- Round-trip mini-truck rate: $r_{\text{diesel\_per\_km}} = ₹22/\text{km}$.
- Hamali loading/unloading: $C_{\text{loading\_per\_qtl}} = ₹35/\text{quintal}$.

### C. Net Realizable Price per Quintal (NRP)
$$\text{NRP}_m = \left[ P_{50} \cdot (1 - L) \cdot (1 - \gamma_{\text{APMC}}) \right] - \frac{C_{\text{transport}}}{Q}$$
- Regional crash condition: $\max_m (\text{NRP}_m) < \text{CostFloor}$ ($\text{CostFloor} = ₹1,100/\text{qtl}$).

### D. WDRA e-NWR Statutory Distress Recovery
- **Current Valuation:** $V = Q \cdot P_{\text{local}} = 50 \times ₹900 = ₹45,000$.
- **Instant Pledge Advance:** $75\% \times V = ₹33,750$ (NABARD Circular 128).
- **Effective Annual Interest:** $7\% - 3\% \text{ (KCC Subvention)} = 4.0\%$.
- **Post-Glut Rebound (10 Days):** Rebound price $P_{\text{rebound}} = ₹1,480/\text{qtl}$.
- **Net Farmer Take-Home:** $50 \times ₹1,480 - ₹5,600 \text{ (storage \& interest)} = ₹68,400$.
- **Net Arbitrage Gain over Panic Sale:** $+₹23,400 \text{ (+52.0\%)}$.

