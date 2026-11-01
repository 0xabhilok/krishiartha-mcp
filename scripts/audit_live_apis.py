import os
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
import time

os.environ['OFFLINE_STAGE_SAFE_MODE'] = 'false'

from mcp_server.chronos_engine import get_weather_covariates, is_offline_mode
from mcp_server.server import calculate_route, get_live_mandi_prices, get_historical_mandi_series

print(f"DEBUG: is_offline_mode = {is_offline_mode()}")

# 1. Open-Meteo
t0 = time.time()
print("\n--- 1. Testing Open-Meteo API ---")
try:
    weather = get_weather_covariates(19.9975, 73.7898)
    dt = time.time() - t0
    print(f"Weather fetched in {dt:.3f}s")
    print(f"Source: {weather.get('source')}")
    print(f"Station: {weather.get('station')}")
    print(f"Current Temp (°C): {weather.get('current_ambient_temp_c')}")
    print(f"Current Humidity (%): {weather.get('current_relative_humidity_pct')}")
    print(f"Past 60d rain total (mm): {weather.get('past_60_days_rainfall_total_mm')}")
    print(f"Forecast 7 days count: {len(weather.get('forecast_7_days', []))}")
except Exception as e:
    print(f"Open-Meteo Error: {e}")

# 2. OSRM Routing
t0 = time.time()
print("\n--- 2. Testing OSRM Highway Routing API ---")
try:
    # Nashik (19.9975, 73.7898) to Surat (21.1702, 72.8311)
    route = calculate_route(19.9975, 73.7898, 21.1702, 72.8311)
    dt = time.time() - t0
    print(f"Route fetched in {dt:.3f}s")
    print(f"Source: {route.get('source')}")
    print(f"Distance (km): {route.get('distance_km')}")
    print(f"Duration (hrs): {route.get('duration_hours')}")
    print(f"GeoJSON coordinates count: {len(route.get('route_geojson', {}).get('coordinates', []))}")
except Exception as e:
    print(f"OSRM Error: {e}")

# 3. Mandi Prices API
t0 = time.time()
print("\n--- 3. Testing Mandi Prices API ---")
try:
    prices = get_live_mandi_prices("Maharashtra", "Tomato")
    dt = time.time() - t0
    print(f"Mandi prices fetched in {dt:.3f}s")
    print(f"Total mandis returned: {len(prices)}")
    for m in prices[:3]:
        print(f" - Mandi: {m.get('market')} ({m.get('district')}), Modal: ₹{m.get('modal_price_inr_per_quintal')}/qtl, Arrival: {m.get('arrival_date')}")
except Exception as e:
    print(f"Mandi API Error: {e}")

# 4. Historical Mandi Prices API
t0 = time.time()
print("\n--- 4. Testing Historical Mandi Series API ---")
try:
    hist = get_historical_mandi_series("Maharashtra", "Tomato", "Pimpalgaon Baswant", days=7)
    dt = time.time() - t0
    print(f"Historical series fetched in {dt:.3f}s")
    print(f"Total records returned: {len(hist)}")
    for h in hist[:2]:
        print(f" - Date: {h.get('date')}, Modal: ₹{h.get('modal_price')}")
except Exception as e:
    print(f"Historical Series Error: {e}")
