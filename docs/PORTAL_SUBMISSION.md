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
- **1-Click Permanent Cloud Deployment (Streamlit Community Cloud):**  
  👉 Deploy in 30 seconds: [Deploy to Streamlit Cloud](https://share.streamlit.io/deploy?repository=0xabhilok/krishiartha-mcp&branch=master&mainModule=frontend/app.py)  
  *(Once deployed, your permanent URL will be `https://krishiartha-mcp.streamlit.app`)*
- **Live Hackathon Stage Tunnel:** `https://krishiartha-forge26.loca.lt` *(Endpoint IP: `152.58.168.161`)*
- **Local Stage Mirror:** `http://localhost:8501`
- **GitHub Repository Source:** `https://github.com/0xabhilok/krishiartha-mcp`

---

### Field 6: Demo video link*
`[Add your unlisted YouTube / Google Drive 5-minute demo video link here]`  
*(Speaker walkthrough script ready in `docs/DEMO_VIDEO_SCRIPT.md`)*

---

### Field 7: Public GitHub*
`https://github.com/0xabhilok/krishiartha-mcp`

---

### Field 8: Presentation / pitch deck link*
- **PowerPoint File:** Included in repo at `docs/KrishiArtha_MCP_Pitch_Deck.pptx`
- **Interactive Web Slide Deck:** Open `docs/PITCH_DECK.html` in any browser or export to PDF
- **Markdown Slide Text:** `docs/PITCH_DECK.md`
- **Shareable Google Drive / Slide Link:** `[Upload docs/KrishiArtha_MCP_Pitch_Deck.pptx to Google Drive / Slides and paste view link here]`

---

## 🏆 Audience Choice Award — Viral Social Media Posts
*(Post on LinkedIn, X/Twitter, and Instagram to score maximum engagement points: 5 pts per Repost, 3 pts per Comment, 1 pt per Like)*

### Option A: LinkedIn Post Copy
```text
🚜 We built KrishiArtha-MCP for FORGE'26 Gen AI Buildathon! 🌾

Did you know Indian smallholder farmers lose over ₹40,000 Crore annually to post-harvest distress sales during unseasonal weather gluts? 

When cloudbursts or unseasonal heatwaves strike, farmers panic-harvest perishable crops (like tomatoes and onions) and dump them in local mandis, crashing prices below production costs. Even worse, hauling crops to distant cities often leads to 18%+ biological rotting in transit due to Arrhenius Q10 thermal decay!

To solve this, Team INFINITE LOOP (IIIT Guwahati) built KrishiArtha-MCP (MandiPulse) — an autonomous, neuro-symbolic multi-agent engine:
🔹 FastMCP Telemetry: Ingests live mandi prices (data.gov.in & mandi-api), Open-Meteo 7-day hourly rain/temp covariates, and OSRM highway routes (Zero Mock Data).
🔹 Time-Series Foundation AI: amazon/chronos-2 generates 10th, 50th, and 90th percentile price quantile forecasts conditioned on weather shocks.
🔹 Thermodynamic Physics: Arrhenius Q10 transit decay + diesel freight deductions expose false arbitrage traps.
🔹 LightRAG Policy & WDRA e-NWR Credit: Unlocks statutory 75% LTV pledge loans @ 4% net interest under NABARD Circular 128, turning a ₹45,000 panic sale into a ₹68,400 rebound (+52% net gain).
🔹 LangGraph v1.2.18 Human-in-the-Loop Gate & Playwright browser agent auto-filing the WDRA portal in 1.21 seconds.
🔹 Multilingual vernacular voice support in Marathi, Hindi, Telugu, and English via Bhashini rails.

🛡️ Audited with AgentShield: Grade A (100/100, 0 vulnerabilities).
🧪 70/70 Pytest test suite passed with 100% offline stage resilience.

Check out our public GitHub repo and live demo:
🔗 GitHub: https://github.com/0xabhilok/krishiartha-mcp
🌐 Live Prototype: https://0e955a783109d3.lhr.life

Built by Abhilok Reddy Bellamkonda & Nimmakayala Naga Venkata Shanmukha Sai Chandra.
Drop your thoughts and support us with a like and repost! 🚀

#GenAI #FORGE26 #AgriTech #LangGraph #Chronos #Bhashini #AIForGood #IIITGuwahati #NxtWave #BuildInPublic
```

### Option B: X (Twitter) Post Copy
```text
🌾 What if farmers could predict mandi crashes 7 days before unseasonal rains hit—and get instant 75% government-backed pledge loans instead of distress dumping?

Proud to launch KrishiArtha-MCP for @NxtWave #FORGE26!

🧠 amazon/chronos-2 foundation time-series forecasting
🔬 Arrhenius Q10 biological transit rot decay math
🏛️ LightRAG hybrid knowledge graph (NABARD Cir 128)
🤝 LangGraph v1.2.18 human-in-the-loop consent gate
🤖 Playwright WDRA e-NWR browser auto-filer (1.21s)
🗣️ Bhashini multilingual speech (Marathi, Hindi, Telugu, English)

Turning ₹45,000 distress dumps into ₹68,400 (+52% income boost).
🛡️ AgentShield: Grade A (100/100)
🧪 70/70 Pytests passing

Live prototype: https://0e955a783109d3.lhr.life
Repo: https://github.com/0xabhilok/krishiartha-mcp

RTs & likes help us win the Audience Choice Award! 🔁❤️

#GenAI #AgriTech #LangGraph #BuildInPublic #AI
```

### Option C: Instagram Caption Copy
```text
Can AI eliminate ₹40,000 Crore of farmer distress sales in India? 🌾🇮🇳

For FORGE'26, our team INFINITE LOOP built KrishiArtha-MCP (MandiPulse) — an autonomous multi-agent AI engine that stops farmers from selling crops at a loss during unseasonal rain gluts.

Instead of generic chatbot math, KrishiArtha uses:
⚡ amazon/chronos-2 foundation model for 7-day weather-conditioned price forecasts
🔬 Real Arrhenius Q10 biological decay physics to predict transit rot
🏛️ Automated government warehouse receipt (e-NWR) loans under NABARD Circular 128
🎙️ Vernacular voice assistance in Marathi, Hindi, Telugu & English

Result: A ₹45,000 loss becomes a ₹68,400 win (+52% net profit).

🔗 Check the link in bio to explore our live prototype and GitHub repo!
Like & share to support our build for FORGE'26! 🚀

#FORGE26 #GenAI #AgriTech #AIForIndia #IIITGuwahati #Engineering #Hackathon #MachineLearning
```
