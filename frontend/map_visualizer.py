"""
KrishiArtha-MCP: PyDeck 3D GIS Mandi Arbitrage Map
Renders interactive arcs and scatter points from farm origin to candidate mandis:
- Green: Recommended WDRA Cold Storage / Profitable Mandi
- Amber: False Arbitrage Trap (High nominal price, severe Q10 transit rot)
- Red: Local Panic Sale (Glut price crash below cost floor)
"""

from typing import Dict, Any, List
import pydeck as pdk


def create_mandi_map(
    farm_lat: float = 19.9975,
    farm_lon: float = 73.7898,
    candidate_mandis: List[Dict[str, Any]] = None,
    warehouse_info: Dict[str, Any] = None,
) -> pdk.Deck:
    """Builds a 3D PyDeck visualization of spatial arbitrage routes."""
    if candidate_mandis is None:
        candidate_mandis = []

    # Origin Farm Pin
    origin_data = [
        {
            "name": "Farm Origin (Nashik)",
            "coordinates": [farm_lon, farm_lat],
            "color": [49, 130, 206],  # Blue
            "size": 180,
            "type": "Origin Farm",
            "desc": "50 Quintals Perishable Tomato Ready for Dispatch",
        }
    ]

    # Mandi Destination Points & Arcs
    mandi_points = []
    arc_data = []

    for mandi in candidate_mandis:
        lat = float(mandi.get("lat", farm_lat))
        lon = float(mandi.get("lon", farm_lon))
        name = mandi.get("market_name", "APMC Market")
        is_local = mandi.get("is_local", False)
        nrp = float(mandi.get("net_realizable_price_per_qtl", 900.0))
        spoilage = float(mandi.get("spoilage_loss_pct", 0.0))
        dist = float(mandi.get("distance_km", 0.0))

        if is_local:
            color = [229, 62, 62]  # Red (Local Crash)
            status_text = "Local Panic Sale (Below Cost Floor)"
        elif dist > 150:
            color = [221, 107, 32]  # Amber/Orange (Surat/Mumbai False Arbitrage)
            status_text = f"False Arbitrage ({spoilage:.1f}% Q10 rot loss)"
        else:
            color = [56, 161, 105]  # Green
            status_text = "Viable Arbitrage"

        mandi_points.append(
            {
                "name": name,
                "coordinates": [lon, lat],
                "color": color,
                "size": 140,
                "type": "APMC Mandi",
                "desc": f"NRP: ₹{nrp:.0f}/qtl | Dist: {dist:.0f}km | Rot: {spoilage:.1f}% | {status_text}",
            }
        )

        arc_data.append(
            {
                "from_name": "Farm Origin",
                "from_coord": [farm_lon, farm_lat],
                "to_name": name,
                "to_coord": [lon, lat],
                "color": color,
            }
        )

    # Warehouse Destination Point & Arc
    if warehouse_info:
        w_lat = 20.0650
        w_lon = 73.9180
        w_name = warehouse_info.get("name", "MSWC Scientific Warehouse, Ozar")
        w_dist = float(warehouse_info.get("distance_km", 14.2))

        mandi_points.append(
            {
                "name": f"⭐ {w_name}",
                "coordinates": [w_lon, w_lat],
                "color": [46, 133, 64],  # Deep Emerald Green
                "size": 220,
                "type": "WDRA Cold Chain Warehouse",
                "desc": f"Recommended: 75% LTV e-NWR Loan | Dist: {w_dist:.1f}km | Zero Rot Loss",
            }
        )

        arc_data.append(
            {
                "from_name": "Farm Origin",
                "from_coord": [farm_lon, farm_lat],
                "to_name": w_name,
                "to_coord": [w_lon, w_lat],
                "color": [46, 133, 64],
            }
        )

    # PyDeck Layers
    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=origin_data + mandi_points,
        get_position="coordinates",
        get_color="color",
        get_radius="size",
        radius_scale=80,
        pickable=True,
    )

    arc_layer = pdk.Layer(
        "ArcLayer",
        data=arc_data,
        get_source_position="from_coord",
        get_target_position="to_coord",
        get_source_color="color",
        get_target_color="color",
        get_width=4,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=farm_lat + 0.3,
        longitude=farm_lon - 0.2,
        zoom=7.5,
        pitch=45,
        bearing=15,
    )

    return pdk.Deck(
        layers=[arc_layer, scatterplot_layer],
        initial_view_state=view_state,
        tooltip={"text": "{name}\n{desc}"},
        map_style="road",
    )
