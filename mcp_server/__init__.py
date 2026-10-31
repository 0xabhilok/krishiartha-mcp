"""
KrishiArtha-MCP Quant Engine Package
Exposes FastMCP server, Chronos-2 covariate forecasting engine,
and Arrhenius Q10 thermodynamic spoilage & spatial arbitrage engine.
"""

from mcp_server.spoilage_arbitrage import (
    calculate_spoilage_rate_k,
    calculate_spoilage_loss,
    calculate_transport_cost,
    calculate_net_realizable_price,
    evaluate_mandi_arbitrage,
)
from mcp_server.chronos_engine import (
    forecast_commodity_price_quantiles,
    get_weather_covariates,
    load_offline_snapshot,
)
from mcp_server.server import (
    mcp,
    get_live_mandi_prices,
    get_historical_mandi_series,
    calculate_route,
    forecast_and_arbitrage,
)

__all__ = [
    "mcp",
    "calculate_spoilage_rate_k",
    "calculate_spoilage_loss",
    "calculate_transport_cost",
    "calculate_net_realizable_price",
    "evaluate_mandi_arbitrage",
    "forecast_commodity_price_quantiles",
    "get_weather_covariates",
    "load_offline_snapshot",
    "get_live_mandi_prices",
    "get_historical_mandi_series",
    "calculate_route",
    "forecast_and_arbitrage",
]
