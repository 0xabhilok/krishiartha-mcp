# KrishiArtha-MCP (MandiPulse)
## Official 5-Minute Video Walkthrough Script (FORGE'26 Evaluation)
**Target Duration:** 5:00 minutes (300 seconds)  
**Presenters:** Abhilok Reddy Bellamkonda & Nimmakayala Sai Chandra (Team INFINITE LOOP, IIIT Guwahati)  

---

### [0:00 – 0:45] Minute 1: The Hook & The Unsolved Crisis
- **Screen:** Webcam showing presenters + Split screen opening to `http://localhost:8501` (KrishiArtha-MCP Cockpit).
- **Speaker (Abhilok):**
  > "Namaste judges. In October 2026, unseasonal torrential rains hit the agricultural belt of Nashik, Maharashtra. Within 48 hours, over 10,000 smallholder farmers panic-harvested their perishable tomatoes, flooding Pimpalgaon and Nashik mandis.
  >
  > Local wholesale clearing prices crashed from ₹1,400 to just ₹900 per quintal—well below the farmer’s production cost of ₹1,100.
  >
  > Why does this disaster repeat every monsoon? Because existing government portals like Agmarknet and eNAM are passive, backward-looking dashboards. They show yesterday’s prices, but they cannot forecast future weather price crashes, they ignore the biological reality of transit spoilage, and they leave the farmer helpless.
  >
  > Today, Team INFINITE LOOP from IIIT Guwahati presents **KrishiArtha-MCP**—the world’s first autonomous multi-agent platform combining foundation time-series forecasting, Arrhenius transit thermodynamics, and statutory distress pledge loans."

---

### [0:45 – 1:45] Minute 2: Multilingual Voice Intake & Live Ingestion
- **Screen:** Screen recording of `http://localhost:8501`. Presenter clicks the Marathi audio trigger button or switches language dropdown.
- **Speaker (Sai Chandra):**
  > "Let's demonstrate live. Our farmer, Suresh Patil from Nashik, has a 50-quintal lot of fresh tomatoes. He speaks in his native tongue:
  >
  > *(Clicks Marathi Trigger)*: *'माझ्याकडे ५० क्विंटल टोमॅटो आहेत, स्थानिक बाजारात भाव पडला आहे.'*
  >
  > Instantly, our Bhashini ULCA layer extracts the slots: Commodity: Tomato, Lot: 50 Quintals, Origin: Nashik (19.99° N, 73.78° E).
  >
  > Behind the scenes, our FastMCP server queries live APIs—zero fake data. It fetches live wholesale prices from `mandi-api.onrender.com` and `data.gov.in`, live 7-day hourly rain and temperature forecasts from Open-Meteo, and live highway distances from OSRM.
  >
  > Notice the weather telemetry: a 42.5mm rainstorm is incoming. Our `amazon/chronos-2` foundation model takes these weather covariates and predicts a severe downside glut: local prices are dropping to ₹620 (P10) and ₹780 (P50)."

---

### [1:45 – 2:45] Minute 3: The Surat Illusion & Arrhenius Q10 Spoilage Physics
- **Screen:** Zoom in on the 3-Column Financial Arbitrage Matrix in the UI.
- **Speaker (Abhilok):**
  > "Now look at the 3-Column Arbitrage Matrix on screen.
  >
  > A conventional AI or broker would look at raw nominal prices and shout: *'Surat APMC is paying ₹1,350 per quintal! Truck your tomatoes 234 kilometers to Gujarat!'*
  >
  > But that is a financial death trap for a farmer. Why?
  >
  > Look at Column B: KrishiArtha models the real-world biological physics. Transporting 50 quintals in an open truck under 31.5°C heat and 82% humidity over 5.2 hours highway driving plus a mandatory 2.5-hour APMC unloading queue triggers aggressive **Arrhenius $Q_{10}$ microbial decay**.
  >
  > The farmer loses **18.4% of total marketable weight**—over 9.2 quintals rot in transit!
  >
  > Add ₹6,800 in round-trip diesel freight ($₹22/\text{km}$), and that flashy ₹1,350 Surat price collapses to an effective net realization of just **₹965 per quintal**—yielding only ₹48,280 net payout. The farmer takes a massive risk for barely ₹3,280 gain."

---

### [2:45 – 3:45] Minute 4: The Breakthrough — LightRAG Policy & LangGraph Interrupt
- **Screen:** Hover over Option C (KrishiArtha Recommended) and show the green LangGraph Consent Card.
- **Speaker (Sai Chandra):**
  > "Because every reachable APMC within 250 kilometers is paying under the ₹1,100 cost floor, KrishiArtha's LangGraph engine triggers a **Regional Distress Crash Flag**.
  >
  > Instead of distress selling, Node 2 activates **LightRAG** in hybrid mode, querying our statutory index of NABARD circulars and WDRA regulations.
  >
  > Look at **Option C**: KrishiArtha discovers the **MSWC Scientific Cold Storage Warehouse** in Ozar, just 14.2 km away.
  >
  > Under **NABARD Circular 128**, Suresh doesn't need to sell today! By depositing his crop and generating an Electronic Negotiable Warehouse Receipt (e-NWR), he gets:
  > 1. An immediate **75% LTV cash advance of ₹33,750** deposited to his bank today.
  > 2. An effective interest rate of **just 4.0% per annum** (7% base minus 3% prompt repayment subvention under Kisan Credit Card).
  > 3. After 10 days, when the monsoon glut clears, tomato prices rebound to ₹1,480/quintal.
  >
  > His net payout after storage rent and interest is **₹68,400**.
  >
  > That is a **+₹23,400 net cash gain—a massive 52% income surge** over local distress selling!"

---

### [3:45 – 4:30] Minute 5: Live Human-in-the-Loop Gate & Automated WDRA Browser Agent
- **Screen:** Presenter clicks the green button: *"Approve e-NWR Loan (होय / हाँ / Approve)"*. The screen shows the Playwright automation executing and opening the WDRA Portal Sanction Slip.
- **Speaker (Abhilok):**
  > "Now watch our agentic governance. In compliance with LangGraph best practices, execution paused cleanly at our `human_approval_gate` with zero side effects.
  >
  > Watch as I click: **'Approve e-NWR Loan'**.
  >
  > `Command(resume=True)` fires! Node 4 launches our automated browser agent.
  >
  > Watch the terminal and browser trace: in **1.21 seconds**, it navigates to the government WDRA e-NWR portal, fills Suresh Patil's Aadhaar and lot parameters, validates the accredited warehouse license, and issues an official digitally signed sanction slip: `WDRA-ENWR-MHNSK20268812-33750.png`!
  >
  > The farmer walks away with immediate liquidity in his pocket and full ownership of his harvest."

---

### [4:30 – 5:00] Wrap-Up: Rubric Compliance & Future Impact
- **Screen:** Show terminal with `70 passed in 7.96s` and AgentShield `Grade A (100/100)`.
- **Speaker (Sai Chandra & Abhilok):**
  > "KrishiArtha-MCP is built to the highest engineering standards:
  > - **Rule 4 Compliance:** 100% live APIs with zero mock data, plus deterministic air-gapped snapshots guaranteeing zero stage failures.
  > - **Security:** Audited via `npx ecc-agentshield scan` with a perfect **Grade A (100/100)** score and zero exposed secrets.
  > - **Testing:** **70 out of 70 unit tests passing** across all modules.
  >
  > By bridging foundation time-series AI, physical logistics thermodynamics, and digital public infrastructure, KrishiArtha transforms agricultural vulnerability into rural economic resilience.
  >
  > Thank you!"
