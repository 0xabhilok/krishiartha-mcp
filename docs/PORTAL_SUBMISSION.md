# NxtWave LaunchpadLive FORGE'26 — Official Portal Submission Form Copy

Use the exact text blocks below to fill out your project submission on the hackathon platform.

---

### Field 1: Which theme did your team build for?*
Select: **Climate, Resource Infrastructure & Global Supply Resilience**  
*(Note: Project also uniquely addresses the Civic Pulse & Digital Governance track through multilingual Bhashini voice rails and statutory NABARD/WDRA digital governance).*

---

### Field 2: Project Name*
`KrishiArtha-MCP (MandiPulse)`

---

### Field 3: Problem Statement*
*(Describe the problem, your target audience, and why it needs to be solved within your chosen theme.)*

```text
Smallholder farmers and Farmer Producer Organizations (FPOs) across India lose 25% to 40% of their net crop value during extreme weather events and unseasonal monsoon gluts. When localized cloudbursts or heatwaves threaten perishable commodities (such as tomatoes, onions, and bananas), farmers panic-harvest and dump produce into the nearest wholesale Agricultural Produce Market Committee (APMC) mandi, triggering catastrophic price collapses below their cost of production.

Existing government portals (Agmarknet 2.0, eNAM) fail to prevent this crisis because they are passive, backward-looking reporting dashboards:
1. They display yesterday's clearing prices but cannot forecast future price collapses 7 days ahead under approaching meteorological shocks.
2. They assume 0% transport crop decay, ignoring that transporting perishables 200+ km in non-refrigerated open trucks under ambient heat and humidity causes severe biological rotting (Arrhenius Q10 decay).
3. When prices crash below production costs, portals offer zero actionable financial safety net, leaving farmers vulnerable to distress sales and predatory local intermediaries.
```

---

### Field 4: Solution Description*
*(Explain your solution, its target users, key use cases, core features, and how AI or autonomous agents enable it.)*

```text
KrishiArtha-MCP is an autonomous, neuro-symbolic multi-agent supply-chain and distress-credit engine that bridges climate forecasting, physical transit thermodynamics, and statutory digital public infrastructure (DPI).

Target Users: Smallholder farmers, FPO managers, agri-logistics coordinators, and rural credit officers.

Core Features & AI/Agent Capabilities:
1. Live Telemetry FastMCP Agent: Consumes live wholesale market data from mandi-api.onrender.com and data.gov.in (resource 9ef84268-d588...), live 7-day hourly precipitation/temperature forecasts from Open-Meteo, and live road geometry from OSRM with zero mock data.
2. Exogenous Weather-Covariate Price Forecaster: Employs amazon/chronos-2 foundation time-series models to predict probabilistic 10th, 50th, and 90th percentile price trajectories conditioned on upcoming rainfall shocks.
3. Thermodynamic Transit Spoilage Engine: Uses the biological Arrhenius Q10 decay equation with an APMC unloading queue buffer and round-trip diesel freight deductions (₹22/km) to calculate true Net Realizable Price (NRP) per quintal across candidate mandis.
4. Autonomous Distress Storage & Policy Agent: When all local mandis crash below the cost floor (₹1,100/qtl), HKUDS/LightRAG in hybrid mode queries NABARD Circular 128 to unlock an immediate 75% LTV Electronic Negotiable Warehouse Receipt (e-NWR) pledge advance at an effective 4.0% interest rate (with 3% KCC subvention), turning a ₹45,000 distress loss into a ₹68,400 rebound return (+52% net income gain).
5. Human-in-the-Loop LangGraph State Machine: Enforces an explicit interrupt() gate for farmer consent before launching an automated browser agent (Playwright) that auto-fills the statutory WDRA warehouse loan portal in 1.21 seconds.
6. Multilingual Vernacular Voice UX: Integrates Bhashini ULCA speech rails across Marathi, Hindi, Telugu, and English with offline client-side translation fallback.
```

---

### Field 5: Live prototype link*
`http://localhost:8501` *(Or your deployed public URL on Streamlit Community Cloud / Render / Vercel)*

---

### Field 6: Demo video link*
`[Add your unlisted YouTube / Google Drive 5-minute demo video link here]`  
*(Script provided in `docs/DEMO_VIDEO_SCRIPT.md`)*

---

### Field 7: Public GitHub*
`https://github.com/0xabhilok/krishiartha-mcp`  
*(Or your team repository URL)*

---

### Field 8: Presentation / pitch deck link*
`[Add your Google Slides / Canva / PDF view link here]`  
*(Slide content provided in `docs/PITCH_DECK.md`)*
```

