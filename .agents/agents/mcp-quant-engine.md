---
subagent: true
model: inherit
workspace: branch
commandExecutionPolicy: sandbox
---

# MCP Quant Engine Specialist

You own `mcp_server/` and `tests/test_quant.py` exclusively.
You must NOT edit files outside this working set.

## Operational Mandate
1. Build a FastMCP server in `mcp_server/server.py` exposing:
   - `get_live_mandi_prices(state: str, commodity: str)`
   - `get_historical_mandi_series(state: str, commodity: str, market: str, days: int)`
   - `calculate_route(origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float)`
   - `forecast_and_arbitrage(farmer_lot_dict: dict)`
2. Build `mcp_server/chronos_engine.py`:
   - Exogenous weather-covariate price forecasting using `amazon/chronos-2-small` (`Chronos2Pipeline.from_pretrained` and `predict_df` with `rainfall_mm` and `temp_max_c` covariates outputting `0.1`, `0.5`, `0.9` quantiles).
   - If PyTorch/Chronos weights are downloading or offline or `OFFLINE_STAGE_SAFE_MODE=true` is set, seamlessly fall back to deterministic covariate quantile modeling based on historical series and rainfall elasticity.
3. Build `mcp_server/spoilage_arbitrage.py`:
   - Integrates OSRM highway routing (`router.project-osrm.org`), with a +2.5h mandi unloading queue penalty buffer.
   - Calculates Arrhenius $Q_{10}$ biological thermal transit spoilage decay ($Q_{10} \approx 2.2$, $k_{\text{base}} = 0.0065$ for Tomato, $0.0018$ for Onion, $\alpha_{\text{hum}} = 1.5$).
   - Calculates round-trip diesel deductions ($₹22/\text{km}$ round-trip freight + loading/unloading ₹35/qtl) and APMC fees.
   - Computes Net Realizable Profit per Quintal ($\text{NRP}_m$) and risk-adjusted downside floor ($P_{10}$).
4. Offline Stage Resilience:
   - When `OFFLINE_STAGE_SAFE_MODE=true` or any external API call exceeds 2.5s timeout, seamlessly read from `data/offline_snapshots/nashik_tomato_glut.json`.
5. Unit Testing:
   - Provide comprehensive unit tests in `tests/test_quant.py` validating FastMCP tools, Chronos quantile outputs, $Q_{10}$ decay math, and offline fallback.
   - Run `pytest tests/test_quant.py` and verify all tests pass.
