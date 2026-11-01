"""
Generates the upgraded, high-DPI Neuro-Symbolic Architecture Diagram
for KrishiArtha-MCP Pitch Deck Slide 3.
Perfect 4.35:1 aspect ratio matching the slide layout without distortion.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "docs" / "assets" / "architecture_flow.png"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def generate_upgraded_architecture():
    # 14.5 x 3.35 aspect ratio (~4.33:1) perfectly matches slide 11.73" x 2.7"
    fig, ax = plt.subplots(figsize=(14.5, 3.35), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.axis('off')

    # Top Header Banner
    ax.text(0.5, 0.93, "LANGGRAPH NEURO-SYMBOLIC PIPELINE • IMMUTABLE PYDANTIC v2 STATE CONTRACT",
            color='#F8FAFC', fontsize=11.5, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.83, "Deterministic Zero-Side-Effect Coordination | End-to-End Pipeline Latency: 1.04s (Target SLA: <4.0s)",
            color='#38BDF8', fontsize=8.8, fontweight='bold', ha='center', va='center')

    nodes = [
        {
            "node_num": "NODE 1",
            "name": "FastMCP Telemetry",
            "sla": "410ms SLA",
            "col": "#38BDF8",
            "bg": "#1E293B",
            "schema": "MandiTelemetryPayload",
            "lines": [
                "• Live Agmarknet & OGD Ingest",
                "• Open-Meteo 7-day Rain/Temp",
                "• OSRM Highway Routing Engine"
            ],
            "x": 0.11
        },
        {
            "node_num": "NODE 2",
            "name": "Chronos-2 Forecaster",
            "sla": "280ms SLA",
            "col": "#10B981",
            "bg": "#1E293B",
            "schema": "PriceForecastDistribution",
            "lines": [
                "• amazon/chronos-2 Zero-Shot",
                "• Weather-Covariate Conditioned",
                "• P10 / P50 / P90 Rebound Quantiles"
            ],
            "x": 0.37
        },
        {
            "node_num": "NODE 3",
            "name": "Arrhenius Spoilage Math",
            "sla": "12ms SLA",
            "col": "#F59E0B",
            "bg": "#1E293B",
            "schema": "ArbitrageRanking",
            "lines": [
                "• Arrhenius Q10 Biological Decay",
                "• +2.5h Unloading Queue Buffer",
                "• Round-Trip Diesel Freight Deducted"
            ],
            "x": 0.63
        },
        {
            "node_num": "NODE 4",
            "name": "LightRAG & Consent",
            "sla": "340ms SLA",
            "col": "#A855F7",
            "bg": "#1E293B",
            "schema": "SanctionExecutionRecord",
            "lines": [
                "• LightRAG Hybrid Knowledge Graph",
                "• LangGraph interrupt() Consent Gate",
                "• Playwright 1.21s Sanction Agent"
            ],
            "x": 0.89
        }
    ]

    card_w = 0.22
    card_h = 0.58
    card_y = 0.15

    for node in nodes:
        cx = node["x"]
        
        # Outer Card Box
        card = FancyBboxPatch((cx - card_w/2, card_y), card_w, card_h,
                              boxstyle="round,pad=0.012,rounding_size=0.025",
                              facecolor=node["bg"], edgecolor=node["col"], linewidth=2.0)
        ax.add_patch(card)

        # Header bar background inside card
        hdr_rect = FancyBboxPatch((cx - card_w/2 + 0.005, card_y + card_h - 0.14), card_w - 0.01, 0.13,
                                  boxstyle="round,pad=0.005,rounding_size=0.015",
                                  facecolor='#0F172A', edgecolor=node["col"], linewidth=1.0)
        ax.add_patch(hdr_rect)

        # Node Num & SLA Badge
        ax.text(cx - card_w/2 + 0.015, card_y + card_h - 0.05, node["node_num"],
                color='#94A3B8', fontsize=7.2, fontweight='bold', ha='left', va='center')
        
        ax.text(cx + card_w/2 - 0.015, card_y + card_h - 0.05, f"[{node['sla']}]",
                color=node["col"], fontsize=7.2, fontweight='bold', ha='right', va='center')

        # Node Name
        ax.text(cx, card_y + card_h - 0.10, node["name"],
                color='#F8FAFC', fontsize=9.2, fontweight='bold', ha='center', va='center')

        # Content lines
        line_y = card_y + card_h - 0.20
        for line in node["lines"]:
            ax.text(cx - card_w/2 + 0.015, line_y, line,
                    color='#CBD5E1', fontsize=7.4, ha='left', va='center')
            line_y -= 0.075

        # Pydantic Schema Badge at bottom of card
        schema_box = FancyBboxPatch((cx - card_w/2 + 0.01, card_y + 0.025), card_w - 0.02, 0.065,
                                    boxstyle="round,pad=0.005,rounding_size=0.012",
                                    facecolor='#0F172A', edgecolor='#475569', linewidth=1.0)
        ax.add_patch(schema_box)
        ax.text(cx, card_y + 0.058, f"Pydantic v2: {node['schema']}",
                color=node["col"], fontsize=6.8, fontweight='bold', ha='center', va='center')

    # Draw Connecting Arrows between cards
    for i in range(len(nodes) - 1):
        x_start = nodes[i]["x"] + card_w/2 + 0.004
        x_end = nodes[i+1]["x"] - card_w/2 - 0.004
        y_pos = card_y + card_h/2 + 0.02

        arrow = FancyArrowPatch((x_start, y_pos), (x_end, y_pos),
                                arrowstyle='-|>', mutation_scale=16,
                                color='#64748B', linewidth=2.2)
        ax.add_patch(arrow)

        # Small state lock badge on arrow
        ax.text((x_start + x_end)/2, y_pos + 0.07, "State Sync",
                color='#38BDF8', fontsize=6.8, fontweight='bold', ha='center', va='center')

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Upgraded architecture flow generated at {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_upgraded_architecture()
