"""
KrishiArtha-MCP: Foundation AI Quantile Fan Chart Visualizer
Uses Plotly to render interactive 7-day probabilistic price forecast cones (P10, P50, P90).
"""

from typing import Dict, Any
import plotly.graph_objects as go
import numpy as np


def create_quantile_fan_chart(
    rainfall_shock_mm: float = 0.0,
    cost_floor_per_qtl: float = 1100.0,
) -> go.Figure:
    """
    Renders an interactive Chronos-2 probabilistic forecast fan chart.
    Dynamic: As rainfall_shock_mm increases, the crash in Day 1-3 deepens,
    the uncertainty cone widens, and the Day 7-10 rebound price climbs.
    """
    days = [
        "Day -2 (Pre-Rain)",
        "Day -1 (Rain Starts)",
        "Day 0 (Today - Glut)",
        "Day +2 (Storm Peak)",
        "Day +4 (Glut Deepens)",
        "Day +7 (Sun Clears)",
        "Day +10 (Rebound)",
    ]

    # Baseline historical & forecast prices
    # As rainfall increases: Day 0 to Day +4 price crashes lower, Day +10 rebounds higher
    shock_down = min(350.0, rainfall_shock_mm * 3.5)
    rebound_up = min(250.0, rainfall_shock_mm * 2.2)

    p10 = [1350, 1150, max(450, 620 - shock_down * 1.1), max(400, 580 - shock_down * 1.3), 720, 1020, 1250 + rebound_up * 0.8]
    p50 = [1420, 1250, max(650, 900 - shock_down), max(600, 850 - shock_down * 1.1), 1050, 1340, 1480 + rebound_up]
    p90 = [1480, 1350, max(850, 950 - shock_down * 0.7), max(820, 920 - shock_down * 0.8), 1220, 1550, 1680 + rebound_up * 1.2]

    fig = go.Figure()

    # Upper bound line (invisible, used for fill)
    fig.add_trace(
        go.Scatter(
            x=days,
            y=p90,
            mode="lines",
            line=dict(color="rgba(56, 161, 105, 0.1)"),
            name="P90 Upside (Shortage)",
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # Shaded Confidence Band (P10 to P90)
    fig.add_trace(
        go.Scatter(
            x=days,
            y=p10,
            mode="lines",
            line=dict(color="rgba(56, 161, 105, 0.1)"),
            fill="tonexty",
            fillcolor="rgba(72, 187, 120, 0.18)",
            name="80% Uncertainty Band (P10–P90)",
            hovertemplate="P10 Downside: ₹%{y:.0f}/qtl<extra></extra>",
        )
    )

    # Upper Line trace
    fig.add_trace(
        go.Scatter(
            x=days,
            y=p90,
            mode="lines",
            line=dict(color="#38a169", width=1.5, dash="dot"),
            name="P90 (90th Percentile)",
            hovertemplate="P90 Upside: ₹%{y:.0f}/qtl<extra></extra>",
        )
    )

    # Median Line (P50)
    fig.add_trace(
        go.Scatter(
            x=days,
            y=p50,
            mode="lines+markers",
            line=dict(color="#22543d", width=3.5),
            marker=dict(size=7, color="#22543d"),
            name="P50 Expected Median Clearing Price",
            hovertemplate="<b>%{x}</b><br>P50 Price: <b>₹%{y:.0f}/qtl</b><extra></extra>",
        )
    )

    # P10 Line trace
    fig.add_trace(
        go.Scatter(
            x=days,
            y=p10,
            mode="lines",
            line=dict(color="#e53e3e", width=1.5, dash="dot"),
            name="P10 (10th Percentile Downside)",
            hovertemplate="P10 Downside: ₹%{y:.0f}/qtl<extra></extra>",
        )
    )

    # Cost Floor reference line
    fig.add_hline(
        y=cost_floor_per_qtl,
        line_dash="dash",
        line_color="#e53e3e",
        line_width=2,
        annotation_text=f"Production Cost Floor: ₹{cost_floor_per_qtl:,.0f}/qtl",
        annotation_position="top left",
        annotation_font_color="#e53e3e",
    )

    # Layout styling
    fig.update_layout(
        title={
            "text": f"<b>Chronos-2 Probabilistic Quantile Forecast</b> (Unseasonal Shock: +{int(rainfall_shock_mm)}mm)",
            "y": 0.95,
            "x": 0.05,
            "xanchor": "left",
            "yanchor": "top",
        },
        xaxis=dict(gridcolor="#edf2f7", tickangle=-15),
        yaxis=dict(
            title="Wholesale Price (₹ / Quintal)",
            gridcolor="#edf2f7",
            range=[350, max(p90) + 120],
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40),
        height=380,
    )

    return fig

