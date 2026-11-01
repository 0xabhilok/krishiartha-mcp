"""
Generates the crystal-clear 'Causal Distress Cycle' diagram
showing the 5-step smallholder panic trap for KrishiArtha-MCP Pitch Deck Slide 2.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ConnectionPatch

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "docs" / "assets" / "causal_distress_cycle.png"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def generate_causal_distress_cycle():
    fig, ax = plt.subplots(figsize=(14.5, 4.4), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.axis('off')

    # Title Banner
    ax.text(0.5, 0.94, "THE SMALLHOLDER CAUSAL DISTRESS CYCLE: HOW UNSEASONAL WEATHER SHOCKS DESTROY WEALTH",
            color='#F8FAFC', fontsize=12.5, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.86, "Empirical breakdown of 50-quintal Nashik tomato harvest during unpredicted monsoon depression",
            color='#94A3B8', fontsize=9.5, ha='center', va='center')

    # 5 Steps Definition
    steps = [
        {
            "num": "01",
            "tag": "CLIMATE SHOCK",
            "title": "Unseasonal\nMonsoon",
            "metric": "48mm / 24h Rain",
            "metric_col": "#38BDF8",
            "desc": "Western Ghats storm front\nZero predictive warning on\nstatic legacy portals",
            "border": "#38BDF8",
            "bg": "#1E293B",
            "x": 0.10
        },
        {
            "num": "02",
            "tag": "PANIC RESPONSE",
            "title": "Premature\nPanic Harvest",
            "metric": "50 Quintals Cut",
            "metric_col": "#F59E0B",
            "desc": "Smallholders panic strip crop\nearly to avoid total fungal\nand mold field rot",
            "border": "#F59E0B",
            "bg": "#1E293B",
            "x": 0.30
        },
        {
            "num": "03",
            "tag": "MARKET COLLAPSE",
            "title": "Local Mandi\nSupply Glut",
            "metric": "₹900 / qtl Crash",
            "metric_col": "#EF4444",
            "desc": "Simultaneous dumping in\nPimpalgaon APMC;\nBelow ₹1,100 cost floor",
            "border": "#EF4444",
            "bg": "#1E293B",
            "x": 0.50
        },
        {
            "num": "04",
            "tag": "TRANSIT ROT TRAP",
            "title": "Highway\nTransport Rot",
            "metric": "18.4% Produce Rot",
            "metric_col": "#F43F5E",
            "desc": "234km Surat transit @ 32°C/85% RH;\n-₹12,420 rot + ₹6,800 diesel\nNet arbitrage collapses",
            "border": "#F43F5E",
            "bg": "#1E293B",
            "x": 0.70
        },
        {
            "num": "05",
            "tag": "DEBT SPIRAL",
            "title": "Predatory\nDistress Debt",
            "metric": "36% APR Loans",
            "metric_col": "#DC2626",
            "desc": "Zero immediate liquidity;\nBorrowing from informal\nloan sharks for next cycle",
            "border": "#DC2626",
            "bg": "#1E293B",
            "x": 0.90
        }
    ]

    card_width = 0.165
    card_height = 0.58
    card_y = 0.20

    for step in steps:
        cx = step["x"]
        # Card Container
        rect = FancyBboxPatch((cx - card_width/2, card_y), card_width, card_height,
                              boxstyle="round,pad=0.015,rounding_size=0.025",
                              facecolor=step["bg"], edgecolor=step["border"], linewidth=2.0)
        ax.add_patch(rect)

        # Micro Category Tag Pill
        tag_rect = FancyBboxPatch((cx - 0.065, card_y + card_height - 0.055), 0.13, 0.042,
                                  boxstyle="round,pad=0.008,rounding_size=0.015",
                                  facecolor='#0F172A', edgecolor=step["border"], linewidth=1.0)
        ax.add_patch(tag_rect)
        ax.text(cx, card_y + card_height - 0.034, f"[{step['tag']}]",
                color=step["border"], fontsize=6.8, fontweight='bold', ha='center', va='center')

        # Step Number & Title
        ax.text(cx, card_y + card_height - 0.11, step["title"],
                color='#F8FAFC', fontsize=10.0, fontweight='bold', ha='center', va='center', linespacing=1.15)

        # Metric Highlight Badge
        metric_rect = FancyBboxPatch((cx - 0.07, card_y + 0.22), 0.14, 0.065,
                                     boxstyle="round,pad=0.008,rounding_size=0.015",
                                     facecolor='#0F172A', edgecolor=step["metric_col"], linewidth=1.2)
        ax.add_patch(metric_rect)
        ax.text(cx, card_y + 0.252, step["metric"],
                color=step["metric_col"], fontsize=9.2, fontweight='bold', ha='center', va='center')

        # Description Bullets / Text
        ax.text(cx, card_y + 0.11, step["desc"],
                color='#CBD5E1', fontsize=7.2, ha='center', va='center', linespacing=1.35)

    # Connecting Arrows between adjacent cards
    for i in range(len(steps) - 1):
        x_start = steps[i]["x"] + card_width/2 + 0.005
        x_end = steps[i+1]["x"] - card_width/2 - 0.005
        y_pos = card_y + card_height/2 + 0.01
        
        arrow = FancyArrowPatch((x_start, y_pos), (x_end, y_pos),
                                arrowstyle='-|>', mutation_scale=16,
                                color='#64748B', linewidth=2.0)
        ax.add_patch(arrow)

    # Bottom Feedback Loop indicating the ongoing systemic cycle
    loop_start_x = steps[4]["x"]
    loop_end_x = steps[0]["x"]
    loop_y = card_y - 0.04
    
    loop_arrow = FancyArrowPatch((loop_start_x, loop_y + 0.03), (loop_end_x, loop_y + 0.03),
                                 connectionstyle="arc3,rad=-0.12",
                                 arrowstyle='-|>', mutation_scale=14,
                                 linestyle='--', color='#EF4444', linewidth=1.6)
    ax.add_patch(loop_arrow)
    ax.text(0.5, loop_y - 0.07, "ANNUAL VICIOUS CYCLE: Smallholders Lose ₹40,000+ Crore Annually to Unhedged Climate Gluts",
            color='#EF4444', fontsize=9.2, fontweight='bold', ha='center', va='center')

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Successfully generated {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_causal_distress_cycle()
