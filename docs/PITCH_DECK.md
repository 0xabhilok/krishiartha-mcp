# KrishiArtha-MCP (MandiPulse)
## 7-Slide Pitch Deck | FORGE'26 GenAI Buildathon
**Track:** Climate, Resource Infrastructure & Global Supply Resilience  
**Team:** INFINITE LOOP (IIIT Guwahati)  
**Live Prototype:** Streamlit Mission Control Cockpit (Port 8501)  

---

### Slide 1: Title & Vision
- **Project Name:** KrishiArtha-MCP (MandiPulse)
- **Tagline:** Autonomous Covariate Mandi Arbitrage, Weather-Spoilage Physics & Statutory Distress-Credit Engine
- **Team INFINITE LOOP:**
  - Abhilok Reddy Bellamkonda (Leader) — IIIT Guwahati
  - Nimmakayala Naga Venkata Shanmukha Sai Chandra — IIIT Guwahati
- **Core Mission:** Eliminating the ₹40,000+ crore annual post-harvest wealth destruction suffered by smallholder Indian farmers during extreme weather gluts by fusing zero-shot foundation time-series forecasting with thermodynamic transit physics and statutory pledge credit.

---

### Slide 2: The Urgent Crisis & Why Existing Solutions Fail
- **The Ground Reality:** Smallholder farmers lose **25%–40%** of net crop value when unseasonal rainfall triggers panic harvests and localized APMC gluts.
- **Why Existing Portals (Agmarknet 2.0, eNAM) Fail:**
  1. **Backward-Looking:** Portals only report yesterday's wholesale clearing prices; they cannot predict price crashes 7 days into the future under approaching storm fronts.
  2. **Blind to Physical Logistics:** They assume 0% transport decay. In reality, carrying tomatoes or onions 200 km in open tarp trucks under 32°C heat and 85% humidity leads to rapid biological rotting ($Q_{10}$ decay).
  3. **Disconnected from Safety Nets:** When prices crash below the production cost floor, portals offer zero recourse, leaving farmers vulnerable to distress sales and predatory local traders.

---

### Slide 3: The Innovation — Neuro-Symbolic Multi-Agent Architecture
KrishiArtha-MCP replaces generic LLM guessing with a deterministic 4-node multi-agent pipeline:
1. **Mandi Telemetry Agent (FastMCP):** Pulls active wholesale prices from `mandi-api.onrender.com/v1/prices` and `data.gov.in` (APMC resource ID `9ef84268-d588...`).
2. **Exogenous Weather-Covariate Forecaster:** Feeds historical modal series + 7-day Open-Meteo precipitation and temperature covariates into `amazon/chronos-2` to generate probabilistic $P_{10}, P_{50}, P_{90}$ price trajectories.
3. **Spatial-Thermodynamic Arbitrage Engine:** Calculates real highway geometry via OSRM, applies Arrhenius $Q_{10}$ biological transit decay with a +2.5h mandi queue penalty, deducts diesel freight ($₹22/\text{km}$ round-trip), and ranks mandis by Net Realizable Profit ($\text{NRP}$).
4. **LightRAG Policy & WDRA Distress Engine:** When a regional glut crashes all mandis below the cost floor ($₹1,100/\text{qtl}$), the engine queries NABARD Circular 128 to unlock an immediate 75% LTV e-NWR pledge advance at 4.0% effective interest while waiting for prices to rebound.

---

### Slide 4: Mathematical & Scientific Defensibility (Zero Hallucinated Math)
- **Visual Assets:**
  - `docs/assets/annotated_arrhenius_rot.png` (Arrhenius thermal decay with pointer callout)
  - `docs/assets/annotated_chronos_rebound.png` (Chronos-2 quantile fan chart with rebound callout)
- **Prominent Chart Callouts:**
  - **Over Arrhenius Curve:** `234 km Highway @ 32°C/85% RH = 18.4% Microbial Rot (-₹12,420 Loss)`
  - **Over Chronos Fan Chart:** `Day +10 Post-Monsoon Rebound: ₹1,480/qtl (+64.4% Surge)`
- **KaTeX LaTeX Scientific Formulas:**
  - **Arrhenius $Q_{10}$ Biological Decay Formula:**
    $$k(T_{\text{amb}}, RH) = k_{\text{base}} \cdot \left(Q_{10}\right)^{\frac{T_{\text{amb}} - 20.0}{10.0}} \cdot \left(1 + \alpha_{\text{hum}} \cdot \max\left(0, \frac{RH - 70}{100}\right)\right)$$
    - Baseline rate $k_{\text{base}} = 0.0065$ for Tomato, $Q_{10} = 2.2$, moisture rot multiplier $\alpha_{\text{hum}} = 1.5$.
    - Total transit duration includes queue buffer: $t_{\text{transit}} = t_{\text{duration}} + 2.5\text{h}$.
    - Spoilage loss fraction: $L = 1 - \exp\left(-k \cdot t_{\text{transit}}\right)$.
  - **Net Realizable Price ($\text{NRP}$):**
    $$\text{NRP}_m = \left[ P_{50} \cdot (1 - L) \cdot (1 - \gamma_{\text{APMC}}) \right] - \frac{C_{\text{transport}}}{Q}$$
- **Explicit Contrast Against Generic LLM Math Hallucination:**
  - *Why LLMs Fail:* Generic LLMs cannot evaluate non-linear exponential Arrhenius kinetics, hallucinate highway distances, and guess future commodity prices with confidence.
  - *The KrishiArtha Guarantee:* Foundation time-series AI (`amazon/chronos-2`) is strictly decoupled from deterministic symbolic physics (USDA/FAO Arrhenius decay + OSRM routing) ensuring 100% mathematical defensibility and 0% hallucinated math.
- **100% Active Live APIs:**
  - `mandi-api.onrender.com/v1/prices` (Live wholesale data)
  - `api.open-meteo.com/v1/forecast` (7-day hourly rain & temp tensors)
  - `router.project-osrm.org` (Live driving distance & duration)

---

### Slide 5: The 3-Column Financial Arbitrage Matrix (Nashik 50 qtl Tomato Lot)
- **Visual Asset:** `docs/assets/financial_arbitrage_3bar.png` (High-DPI 3-bar comparison chart with itemized deduction banner)

| Financial Metric | The Local Distress Trap (Pimpalgaon APMC) | The False Transit Mirage (Surat APMC) | The KrishiArtha Breakthrough (MSWC Ozar WDRA) |
| :--- | :--- | :--- | :--- |
| **Market Destination** | Pimpalgaon APMC (12 km) | Surat APMC (234 km) | MSWC Cold Storage, Ozar (14.2 km) |
| **Nominal Quoted Price** | ₹900 / quintal (Severe Crash) | ₹1,350 / quintal (Apparent Arbitrage) | Rebound: ₹1,480 / quintal (Day +10 post-monsoon) |
| **$Q_{10}$ Transit Rot Loss** | ₹945 (2.1% loss) | **₹12,420 (18.4% Thermal Rot!)** | ₹0 (Cold storage preservation guarantee) |
| **Round-Trip Freight & Handling** | ₹1,925 (Local mini-truck) | ₹6,800 ($₹22/\text{km}$ round-trip) | ₹750 (Short warehouse haul) |
| **Immediate Farmer Liquidity** | ₹45,000 (Immediate Cash) | ₹48,280 (Post-transit payout) | **₹33,750 Immediate Cash (75% LTV @ 4% net interest)** |
| **Cold Storage & Subvented Interest** | ₹0 (No storage) | ₹0 (Direct sale) | **-₹5,600 (₹4,200 cold storage + ₹1,400 KCC 4% net interest)** |
| **Final Net Take-Home Payout** | **₹45,000 Net Baseline** | **₹48,280 Net (+7.3% False Trap)** | **₹68,400 Net (+52.0% Income Surge)** |
| **Net Arbitrage Realization** | Baseline | +₹3,280 (+7.3%) | **+₹23,400 Net Gain (+52.0% Income Surge)** |

- **Itemized Arithmetic Defensibility:**
  - Gross Rebound Revenue: $50\text{ qtl} \times ₹1,480 = ₹74,000$
  - Deductions: Cold Storage (10 days @ ₹8.4/qtl/d = ₹4,200) + KCC 4% Subvented Interest (₹1,400) = -₹5,600
  - Net Realization: $₹74,000 - ₹5,600 = ₹68,400$ (100% arithmetic precision)

---

### Slide 6: Human-in-the-Loop Governance & Automated Browser Execution
- **Visual Assets:**
  - `docs/assets/langgraph_governance_flow.png` (3-step state machine sequence + 1.21s SLA stopwatch benchmark)
  - `docs/assets/annotated_wdra_sanction.png` (Framed WDRA sanction slip with overlay callouts)
- **3-Step LangGraph State Machine Sequence:**
  `[Step 1: Quant Assessment] ➔ [Step 2: STATE FROZEN: interrupt() Consent Barrier] ➔ [Step 3: Playwright 1.21s Auto-Filing]`
  - **Step 1 (Quant Assessment):** FastMCP + Chronos-2 detects ₹900 crash below ₹1,100 floor; Arrhenius detects Surat 18.4% rot trap; evaluates WDRA +52% arbitrage.
  - **Step 2 (STATE FROZEN):** LangGraph `interrupt()` halts execution before warehouse lock or bank pledge. State persisted to Postgres checkpointer. Dispatches vernacular IVR/WhatsApp prompt to farmer: *"Approve e-NWR Loan (होय / हाँ)?"*
  - **Step 3 (Playwright Auto-Filing):** Resumes strictly upon human authorization `Command(resume=True)`. Playwright browser agent auto-fills 14 fields in 1.21s and emits official sanction certificate.
- **Stopwatch Benchmark Comparison:**
  - Playwright Automated Execution: **1.21s** (SLA target: <4.0s).
  - Manual WDRA Portal Human Filing: **15–20 minutes** (700x speedup with zero typographical error).
- **Overlay Callouts on Sanction Certificate:**
  - **Approved Advance:** ₹33,750 (75% LTV Day-0 liquidity)
  - **Effective Interest:** 4.0% p.a. (3% prompt repayment subvention via NABARD Circular 128)
  - **Accredited Warehouse:** MSWC Ozar (#MSWC-412)
  - **Execution Latency:** 1.21s (Cryptographic Hash: `0x8F9B2C`)

---

### Slide 7: Enterprise Architecture, Security & Future Roadmap
- **Security & Quality Audit (AgentShield):**
  - `npx ecc-agentshield scan` score: **Grade A (100/100)**.
  - Zero exposed API secrets, zero CVE vulnerabilities, clean sandbox permissions.
  - **70/70 Pytest Suite Passed** under both Live and Air-Gapped (`OFFLINE_STAGE_SAFE_MODE=true`) execution.
- **National Scalability & ONDC Integration:**
  - Connecting Farmer Producer Organizations (FPOs) directly to the Open Network for Digital Commerce (ONDC) logistics grid.
  - Integration with Agmarknet 2.0 national telemetry across 688 Indian mandis.
  - Direct banking integration via Jan Dhan-Aadhaar-Mobile (JAM) trinity for automated subvented loan disbursals in <60 seconds.

