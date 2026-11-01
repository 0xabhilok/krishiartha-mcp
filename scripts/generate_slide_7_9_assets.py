"""
Asset generation script for Slide 7, 8, 9 of KrishiArtha-MCP Pitch Deck.
Generates:
1. docs/assets/whatsapp_vernacular_card.png
2. docs/assets/national_dpi_architecture.png
3. docs/assets/security_shield_badges.png
4. docs/assets/dual_qr_evaluation.png
"""

import os
import math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import qrcode

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = REPO_ROOT / "docs" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Fonts helper
def get_font(size, bold=False, marathi=False):
    try:
        if marathi:
            font_path = "C:/Windows/Fonts/Nirmala.ttc"
            idx = 1 if bold else 0
            return ImageFont.truetype(font_path, size, index=idx)
        else:
            if bold:
                for p in ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/Nirmala.ttc"]:
                    if os.path.exists(p):
                        idx = 1 if "Nirmala" in p else 0
                        return ImageFont.truetype(p, size, index=idx)
            else:
                for p in ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/Nirmala.ttc"]:
                    if os.path.exists(p):
                        return ImageFont.truetype(p, size)
    except Exception as e:
        print(f"Font loading fallback: {e}")
    return ImageFont.load_default()

# ------------------------------------------------------------------------------
# 1. Smartphone Vernacular WhatsApp Voice Note Card
# ------------------------------------------------------------------------------
def generate_whatsapp_vernacular_card():
    w, h = 1000, 1280
    img = Image.new("RGBA", (w, h), (15, 23, 42, 255)) # Dark navy background
    draw = ImageDraw.Draw(img)

    # Smartphone Outer Chassis / Frame
    phone_x0, phone_y0 = 60, 30
    phone_x1, phone_y1 = 940, 1250
    # Outer bezel glow
    draw.rounded_rectangle([phone_x0-6, phone_y0-6, phone_x1+6, phone_y1+6], radius=46, fill=(16, 185, 129, 40), outline=(16, 185, 129, 80), width=2)
    # Phone body
    draw.rounded_rectangle([phone_x0, phone_y0, phone_x1, phone_y1], radius=40, fill=(11, 20, 26, 255), outline=(51, 65, 85, 255), width=3)

    # Smartphone Notch / Dynamic Island
    draw.rounded_rectangle([420, phone_y0 + 12, 580, phone_y0 + 36], radius=12, fill=(2, 6, 23, 255))
    draw.ellipse([550, phone_y0 + 18, 562, phone_y0 + 30], fill=(30, 41, 59, 255)) # camera dot

    # Phone Status Bar
    font_status = get_font(18, bold=True)
    draw.text((phone_x0 + 40, phone_y0 + 16), "09:42", fill=(203, 213, 225, 255), font=font_status)
    draw.text((phone_x1 - 140, phone_y0 + 16), "5G  89%", fill=(203, 213, 225, 255), font=font_status)

    # WhatsApp Header Bar
    wh_y0 = phone_y0 + 48
    wh_y1 = wh_y0 + 90
    draw.rectangle([phone_x0 + 3, wh_y0, phone_x1 - 3, wh_y1], fill=(18, 30, 38, 255))
    draw.line([phone_x0 + 3, wh_y1, phone_x1 - 3, wh_y1], fill=(30, 41, 59, 255), width=2)

    # Avatar Circle
    av_x = phone_x0 + 40
    av_y = wh_y0 + 16
    draw.ellipse([av_x, av_y, av_x + 56, av_y + 56], fill=(16, 185, 129, 255))
    draw.text((av_x + 13, av_y + 11), "🌾", font=get_font(28))

    # Header Contact Text
    draw.text((av_x + 72, av_y + 4), "कृषीअर्थ सहाय्यक (KrishiArtha Bot)", fill=(248, 250, 252, 255), font=get_font(22, bold=True, marathi=True))
    draw.text((av_x + 72, av_y + 32), "🟢 Verified DPI Agricultural Assistant • ऑनलाइन", fill=(52, 211, 153, 255), font=get_font(15, marathi=True))

    # Top Date Pill
    date_pill_y = wh_y1 + 25
    draw.rounded_rectangle([430, date_pill_y, 570, date_pill_y + 32], radius=16, fill=(24, 34, 41, 255), outline=(51, 65, 85, 255), width=1)
    draw.text((472, date_pill_y + 5), "आज (Today)", fill=(148, 163, 184, 255), font=get_font(14, bold=True, marathi=True))

    # Message 1: Alert Bubble
    m1_y0 = date_pill_y + 48
    m1_y1 = m1_y0 + 115
    draw.rounded_rectangle([phone_x0 + 30, m1_y0, phone_x1 - 60, m1_y1], radius=18, fill=(31, 44, 52, 255), outline=(239, 68, 68, 180), width=1)
    # Alert icon & heading
    draw.text((phone_x0 + 50, m1_y0 + 12), "🚨 नाशिक हवामान व हमीभाव चेतावणी (Nashik Tomato Alert)", fill=(248, 113, 113, 255), font=get_font(20, bold=True, marathi=True))
    draw.text((phone_x0 + 50, m1_y0 + 44), "शेतकरी रमेश, पिंपळगाव समितीत भाव ₹९००/क्विंटलवर घसरले आहेत (उत्पादन खर्च ₹१,१००).\nतो तात्काळ टाळण्यासाठी खालील अधिकृत व्हॉइस मेसेज ऐका:", fill=(226, 232, 240, 255), font=get_font(16, marathi=True))
    draw.text((phone_x1 - 130, m1_y1 - 25), "09:41 AM", fill=(148, 163, 184, 255), font=get_font(13))

    # Message 2: Vernacular WhatsApp Audio Note Card (The Primary Hero Feature)
    vn_y0 = m1_y1 + 24
    vn_y1 = vn_y0 + 490
    draw.rounded_rectangle([phone_x0 + 30, vn_y0, phone_x1 - 40, vn_y1], radius=22, fill=(20, 48, 45, 255), outline=(16, 185, 129, 255), width=2)

    # Voice Note Header Banner
    draw.rounded_rectangle([phone_x0 + 45, vn_y0 + 15, phone_x1 - 55, vn_y0 + 55], radius=10, fill=(16, 185, 129, 45))
    draw.text((phone_x0 + 60, vn_y0 + 22), "🎙️ अधिकृत मराठी व्हॉइस सल्लागार (Bhashini ULCA Voice Engine)", fill=(52, 211, 153, 255), font=get_font(17, bold=True, marathi=True))

    # Audio Waveform Player Row
    aw_y = vn_y0 + 75
    # Play Button Circle
    pb_x, pb_y = phone_x0 + 60, aw_y + 10
    draw.ellipse([pb_x, pb_y, pb_x + 64, pb_y + 64], fill=(16, 185, 129, 255), outline=(52, 211, 153, 255), width=2)
    # White Play Triangle
    draw.polygon([(pb_x + 25, pb_y + 18), (pb_x + 25, pb_y + 46), (pb_x + 46, pb_y + 32)], fill=(255, 255, 255, 255))

    # Acoustic Waveform Bars (Dynamic Amplitude Bars)
    wave_x_start = pb_x + 85
    num_bars = 36
    bar_width = 8
    bar_gap = 4
    np.random.seed(42)
    heights = [14, 22, 38, 52, 35, 48, 60, 42, 28, 50, 62, 58, 45, 30, 48, 55, 40, 26, 34, 46, 52, 38, 24, 32, 44, 50, 36, 22, 30, 42, 48, 35, 20, 28, 34, 18]

    # First 16 bars are played (Emerald), remaining are unplayed (Muted Slate)
    for i in range(num_bars):
        bx = wave_x_start + i * (bar_width + bar_gap)
        bh = heights[i]
        by0 = aw_y + 42 - (bh // 2)
        by1 = aw_y + 42 + (bh // 2)
        b_color = (16, 185, 129, 255) if i < 16 else (100, 116, 139, 255)
        draw.rounded_rectangle([bx, by0, bx + bar_width, by1], radius=3, fill=b_color)

    # Small Avatar Indicator on Waveform (showing playback cursor)
    cursor_x = wave_x_start + 16 * (bar_width + bar_gap)
    draw.ellipse([cursor_x - 7, aw_y + 35, cursor_x + 7, aw_y + 49], fill=(52, 211, 153, 255), outline=(255, 255, 255, 255), width=2)

    # Audio Timestamps & Double Tick
    draw.text((wave_x_start, aw_y + 78), "0:42 / 1:15", fill=(16, 185, 129, 255), font=get_font(16, bold=True))
    draw.text((phone_x1 - 165, aw_y + 78), "09:42 AM  ✓✓", fill=(56, 189, 248, 255), font=get_font(15, bold=True))

    # Transcript Box in Marathi (Quoted verbatim from Audit Report)
    tr_y0 = aw_y + 115
    draw.rounded_rectangle([phone_x0 + 50, tr_y0, phone_x1 - 60, tr_y0 + 175], radius=14, fill=(15, 34, 38, 255), outline=(52, 211, 153, 140), width=1)
    
    quote_text_mr = '"शेतकरी रमेश: टोमॅटो विकू नका! ओझर गोदामात ठेवा, ₹३३,७५० तात्काळ कर्ज मिळवा (४% व्याज)."'
    draw.text((phone_x0 + 68, tr_y0 + 14), quote_text_mr, fill=(254, 240, 138, 255), font=get_font(21, bold=True, marathi=True))

    # Detailed Points
    p1 = "• पिंपळगाव स्थानिक तोटा: ₹४५,००० (किंमत उत्पादन खर्चाखाली)"
    p2 = "• ओझर गोदामात साठवणूक: ₹३३,७५० रोख उचल आजच KCC खात्यावर"
    p3 = "• १० दिवसांत भाव उसळी (Chronos-2): ₹१,४८०/क्विंटल -> निव्वळ नफा ₹६८,४०० (+५२.०%)"
    draw.text((phone_x0 + 68, tr_y0 + 56), p1, fill=(248, 113, 113, 255), font=get_font(16, marathi=True))
    draw.text((phone_x0 + 68, tr_y0 + 90), p2, fill=(52, 211, 153, 255), font=get_font(16, bold=True, marathi=True))
    draw.text((phone_x0 + 68, tr_y0 + 124), p3, fill=(56, 189, 248, 255), font=get_font(16, bold=True, marathi=True))

    # Interactive Action Buttons Inside WhatsApp Card
    btn_y0 = tr_y0 + 195
    # Button 1: Approve WDRA Loan (Primary Call to Action)
    draw.rounded_rectangle([phone_x0 + 50, btn_y0, phone_x1 - 60, btn_y0 + 50], radius=12, fill=(16, 185, 129, 255))
    draw.text((phone_x0 + 140, btn_y0 + 10), "✅ होय, ई-एनडब्ल्यूआर कर्ज मंजूर करा (Approve e-NWR)", fill=(2, 44, 34, 255), font=get_font(18, bold=True, marathi=True))

    # Button 2: Talk to Agri-Advisor in Marathi
    btn_y1 = btn_y0 + 60
    draw.rounded_rectangle([phone_x0 + 50, btn_y1, phone_x1 - 60, btn_y1 + 46], radius=12, fill=(30, 41, 59, 255), outline=(148, 163, 184, 200), width=1)
    draw.text((phone_x0 + 175, btn_y1 + 10), "📞 कृषी सल्लागाराशी बोला (Talk in Marathi)", fill=(241, 245, 249, 255), font=get_font(17, marathi=True))

    # Bottom Multilingual Speech Rails Badge
    ft_y0 = vn_y1 + 25
    draw.rounded_rectangle([phone_x0 + 30, ft_y0, phone_x1 - 40, ft_y0 + 65], radius=14, fill=(15, 23, 42, 255), outline=(56, 189, 248, 160), width=1)
    draw.text((phone_x0 + 48, ft_y0 + 10), "🌐 Bhashini ULCA Multilingual Speech Rails", fill=(56, 189, 248, 255), font=get_font(16, bold=True))
    draw.text((phone_x0 + 48, ft_y0 + 34), "मराठी (Marathi)  •  हिन्दी (Hindi)  •  తెలుగు (Telugu)  •  English  •  22 Scheduled Languages", fill=(203, 213, 225, 255), font=get_font(14, marathi=True))

    out_path = ASSETS_DIR / "whatsapp_vernacular_card.png"
    img.save(out_path, dpi=(300, 300))
    print(f"[OK] Generated {out_path} ({w}x{h})")

# ------------------------------------------------------------------------------
# 2. National DPI Architecture Diagram
# ------------------------------------------------------------------------------
def generate_national_dpi_architecture():
    fig, ax = plt.subplots(figsize=(16, 8.5), dpi=300)
    fig.patch.set_facecolor('#0b1329')
    ax.set_facecolor('#0b1329')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Title Banner
    ax.text(8.0, 8.0, "KRISHIARTHA-MCP: NATIONAL DIGITAL PUBLIC INFRASTRUCTURE (DPI) INTERCONNECT",
            fontsize=15, fontweight='bold', color='#f8fafc', ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", fc="#0f172a", ec="#38bdf8", lw=1.5))

    # Helper for styled box
    def draw_card(x, y, w, h, title, subtitle, items, border_color, fill_color='#131f37', badge=None):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15,rounding_size=0.2",
                                      facecolor=fill_color, edgecolor=border_color, linewidth=2, zorder=2)
        ax.add_patch(rect)
        
        # Badge
        if badge:
            ax.text(x + w - 0.2, y + h - 0.25, badge, fontsize=8.5, fontweight='bold', color=border_color,
                    ha='right', va='center', bbox=dict(boxstyle="round,pad=0.25", fc="#0b1329", ec=border_color, lw=1), zorder=4)

        ax.text(x + 0.3, y + h - 0.45, title, fontsize=12, fontweight='bold', color='#f8fafc', va='center', zorder=4)
        ax.text(x + 0.3, y + h - 0.85, subtitle, fontsize=9.5, fontweight='bold', color=border_color, va='center', zorder=4)
        
        # Separator line
        ax.plot([x + 0.3, x + w - 0.3], [y + h - 1.1, y + h - 1.1], color=border_color, alpha=0.4, lw=1, zorder=4)
        
        # Item bullets
        curr_y = y + h - 1.45
        for item in items:
            ax.text(x + 0.3, curr_y, item, fontsize=8.8, color='#cbd5e1', va='center', zorder=4)
            curr_y -= 0.38

    # Column 1: Upstream DPI & Environmental Ingestion (x=0.6, w=4.2)
    ax.text(2.7, 7.3, "UPSTREAM TELEMETRY & CLIMATE DPI", fontsize=11, fontweight='bold', color='#38bdf8', ha='center', va='center')
    
    draw_card(0.6, 4.0, 4.2, 2.9,
              "Agmarknet 2.0 (DPI Telemetry)",
              "National APMC Mandi Wholesale Ingestion",
              ["• 688 APMC Mandis across 28 States & UTs",
               "• Resource IDs: 9ef84268... & 35985678...",
               "• Live modal, min, max wholesale rates",
               "• Latency SLA: 410ms with zero fake data"],
              border_color='#38bdf8', badge="OGD INDIA")

    draw_card(0.6, 0.7, 4.2, 2.9,
              "Open-Meteo Climate Engine",
              "Hyper-Local Weather Covariates",
              ["• 7-Day hourly precipitation & rain tensors",
               "• High-resolution ambient temperature & RH%",
               "• Early storm front & glut surge warning",
               "• Arrhenius kinetic temperature feeds"],
              border_color='#0284c7', badge="ATMOSPHERIC DPI")

    # Column 2: KrishiArtha Multi-Agent Brain (x=5.6, w=4.8)
    ax.text(8.0, 7.3, "KRISHIARTHA NEURO-SYMBOLIC BRAIN", fontsize=11, fontweight='bold', color='#10b981', ha='center', va='center')

    # Brain Container Box
    brain_box = patches.FancyBboxPatch((5.5, 0.6), 5.0, 6.4, boxstyle="round,pad=0.2,rounding_size=0.25",
                                       facecolor='#0f2337', edgecolor='#10b981', linewidth=2.5, zorder=2)
    ax.add_patch(brain_box)

    # 4 Inner Agent Blocks inside Brain
    draw_card(5.8, 5.3, 4.4, 1.4,
              "1. FastMCP Telemetry Agent (410ms)",
              "Deterministic Schema Validation",
              ["• Pydantic v2 ArbitrageState contracts",
               "• Offline snapshot fallback resilience"],
              border_color='#10b981', fill_color='#132d3d')

    draw_card(5.8, 3.8, 4.4, 1.4,
              "2. amazon/chronos-2 Forecaster (280ms)",
              "Foundation Time-Series Model",
              ["• Pretrained zero-shot T5 quantile decoder",
               "• Probabilistic P10, P50, P90 price paths"],
              border_color='#34d399', fill_color='#132d3d')

    draw_card(5.8, 2.3, 4.4, 1.4,
              "3. Spatial-Thermodynamic Engine (12ms)",
              "Arrhenius Q10 Decay + OSRM Routing",
              ["• Exponential decay + 2.5h queue buffer",
               "• Net Realizable Price (NRP) ranking"],
              border_color='#10b981', fill_color='#132d3d')

    draw_card(5.8, 0.8, 4.4, 1.4,
              "4. Policy Core & LangGraph interrupt() (340ms)",
              "LightRAG + Statutory Consent Barrier",
              ["• NABARD Circular 128 (75% LTV @ 4% net)",
               "• Playwright automated e-NWR browser agent"],
              border_color='#6ee7b7', fill_color='#132d3d')

    # Column 3: Downstream DPI Execution (x=11.2, w=4.2)
    ax.text(13.3, 7.3, "DOWNSTREAM EXECUTION & FARMER DISBURSAL", fontsize=11, fontweight='bold', color='#f59e0b', ha='center', va='center')

    draw_card(11.2, 4.0, 4.2, 2.9,
              "ONDC Logistics Grid",
              "Open Highway Mini-Truck Dispatch",
              ["• Unified digital fleet booking across ONDC",
               "• Real-time round-trip diesel calculation (₹22/km)",
               "• Hamali handling deduction (₹35/qtl)",
               "• Verified transit route optimization"],
              border_color='#f59e0b', badge="ONDC NETWORK")

    draw_card(11.2, 0.7, 4.2, 2.9,
              "WDRA & JAM Financial Trinity",
              "Statutory Subvented Pledge Liquidity",
              ["• Instant 75% LTV e-NWR warehouse advance",
               "• Jan Dhan - Aadhaar - Mobile direct disbursal",
               "• 4.0% net interest (3% prompt subvention)",
               "• Eliminates 36% predatory moneylenders"],
              border_color='#10b981', badge="WDRA / NABARD")

    # Connective Arrows between Tiers
    arrow_props = dict(boxstyle="square", fc="#0b1329", ec="none")
    # Agmarknet -> Brain
    ax.annotate("", xy=(5.5, 5.5), xytext=(4.8, 5.5),
                arrowprops=dict(arrowstyle="-|>", color='#38bdf8', lw=2.5, mutation_scale=18))
    ax.text(5.15, 5.75, "Wholesale Rates", fontsize=7.5, color='#38bdf8', ha='center', fontweight='bold')

    # Weather -> Brain
    ax.annotate("", xy=(5.5, 2.2), xytext=(4.8, 2.2),
                arrowprops=dict(arrowstyle="-|>", color='#0284c7', lw=2.5, mutation_scale=18))
    ax.text(5.15, 2.45, "Rain Covariates", fontsize=7.5, color='#0284c7', ha='center', fontweight='bold')

    # Brain -> ONDC
    ax.annotate("", xy=(11.2, 5.5), xytext=(10.5, 5.5),
                arrowprops=dict(arrowstyle="-|>", color='#f59e0b', lw=2.5, mutation_scale=18))
    ax.text(10.85, 5.75, "Transit Booking", fontsize=7.5, color='#f59e0b', ha='center', fontweight='bold')

    # Brain -> WDRA
    ax.annotate("", xy=(11.2, 2.2), xytext=(10.5, 2.2),
                arrowprops=dict(arrowstyle="-|>", color='#10b981', lw=2.5, mutation_scale=18))
    ax.text(10.85, 2.45, "Pledge Sanction", fontsize=7.5, color='#10b981', ha='center', fontweight='bold')

    plt.tight_layout()
    out_path = ASSETS_DIR / "national_dpi_architecture.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {out_path}")

# ------------------------------------------------------------------------------
# 3. Security Shield Badges
# ------------------------------------------------------------------------------
def generate_security_shield_badges():
    fig, ax = plt.subplots(figsize=(16, 5.2), dpi=300)
    fig.patch.set_facecolor('#0b1329')
    ax.set_facecolor('#0b1329')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 5.2)
    ax.axis('off')

    def draw_shield_icon(cx, cy, scale, color):
        # Draw a custom stylized vector shield
        shield_pts = np.array([
            [cx - 0.35 * scale, cy + 0.4 * scale],
            [cx + 0.35 * scale, cy + 0.4 * scale],
            [cx + 0.35 * scale, cy - 0.05 * scale],
            [cx, cy - 0.45 * scale],
            [cx - 0.35 * scale, cy - 0.05 * scale]
        ])
        shield_poly = patches.Polygon(shield_pts, closed=True, facecolor='#0b1329', edgecolor=color, linewidth=2.2, zorder=5)
        ax.add_patch(shield_poly)

    def draw_badge_card(x, y, w, h, emblem_text, badge_name, score_text, subtitle, bullets, theme_color, bg_card='#101e38'):
        # Card container
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15,rounding_size=0.25",
                                      facecolor=bg_card, edgecolor=theme_color, linewidth=2.2, zorder=2)
        ax.add_patch(rect)

        # Draw vector shield icon at header
        draw_shield_icon(x + 0.7, y + h - 0.65, scale=1.1, color=theme_color)
        ax.text(x + 0.7, y + h - 0.65, emblem_text, fontsize=12, fontweight='bold', color=theme_color, ha='center', va='center', zorder=6)

        # Header Title
        ax.text(x + 1.25, y + h - 0.5, badge_name, fontsize=12.5, fontweight='bold', color='#f8fafc', va='center', zorder=4)
        ax.text(x + 1.25, y + h - 0.85, subtitle, fontsize=9.2, color='#94a3b8', va='center', zorder=4)

        # Score Pill
        ax.text(x + w - 0.4, y + h - 0.65, score_text, fontsize=11, fontweight='bold', color='#0b1329',
                ha='right', va='center', bbox=dict(boxstyle="round,pad=0.35", fc=theme_color, ec="none"), zorder=4)

        # Divider line
        ax.plot([x + 0.4, x + w - 0.4], [y + h - 1.2, y + h - 1.2], color=theme_color, alpha=0.5, lw=1.2, zorder=4)

        # Bullets
        curr_y = y + h - 1.6
        for b in bullets:
            ax.text(x + 0.4, curr_y, b, fontsize=9.2, color='#e2e8f0', va='center', zorder=4)
            curr_y -= 0.42

    # Badge 1: AgentShield Grade A (100/100)
    draw_badge_card(
        x=0.5, y=0.4, w=4.7, h=4.4,
        emblem_text="A+",
        badge_name="AgentShield Certified",
        score_text="GRADE A (100/100)",
        subtitle="Autonomous Agent Security Audit",
        bullets=[
            "• Zero Hardcoded Secrets & API Key Leaks",
            "• Zero Prompt Injection Attack Vectors",
            "• Zero Supply-Chain Vulnerabilities & CVEs",
            "• Strict Least-Privilege FastMCP Tool Sandboxing",
            "• Audited via npx ecc-agentshield scan standard"
        ],
        theme_color='#10b981',
        bg_card='#0f2824'
    )

    # Badge 2: 70/70 Pytest Verification Suite
    draw_badge_card(
        x=5.65, y=0.4, w=4.7, h=4.4,
        emblem_text="70",
        badge_name="70/70 Pytest Rig",
        score_text="100% PASS (11.3s)",
        subtitle="End-to-End Test Suite Execution",
        bullets=[
            "• 23 FastMCP & Quant Thermodynamic Tests",
            "• 18 LightRAG Policy & NABARD Rule Tests",
            "• 10 LangGraph StateGraph & interrupt() Tests",
            "• 19 Streamlit UI & Vernacular Audio Tests",
            "• Deterministic local snapshot regression certified"
        ],
        theme_color='#38bdf8',
        bg_card='#0d233a'
    )

    # Badge 3: Pydantic v2 Symbolic Sandbox
    draw_badge_card(
        x=10.8, y=0.4, w=4.7, h=4.4,
        emblem_text="P2",
        badge_name="Pydantic v2 Sandbox",
        score_text="ZERO LLM MATH",
        subtitle="Deterministic Mathematical Defensibility",
        bullets=[
            "• Zero Hallucinated Math in Arbitrage Decisions",
            "• Strongly Typed Schemas (ArbitrageState)",
            "• Decimal Precision Financial & Tax Ledger",
            "• Pure Python Arrhenius & Diesel Freight Physics",
            "• Tamper-Proof Cryptographic Sanction Hashes"
        ],
        theme_color='#f59e0b',
        bg_card='#261f12'
    )

    plt.tight_layout()
    out_path = ASSETS_DIR / "security_shield_badges.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {out_path}")

# ------------------------------------------------------------------------------
# 4. Dual QR Code Evaluation Asset
# ------------------------------------------------------------------------------
def generate_dual_qr_evaluation():
    w, h = 1200, 560
    img = Image.new("RGBA", (w, h), (11, 19, 41, 255))
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rounded_rectangle([15, 15, w - 15, h - 15], radius=24, fill=(15, 23, 42, 255), outline=(56, 189, 248, 160), width=2)

    # QR 1: Live Web Prototype
    qr1 = qrcode.QRCode(version=1, box_size=8, border=2)
    qr1.add_data("https://krishiartha-mcp.streamlit.app")
    qr1.make(fit=True)
    img_qr1 = qr1.make_image(fill_color="#0f172a", back_color="#ffffff").convert("RGBA")

    # QR 2: Masterpiece Demo Video
    qr2 = qrcode.QRCode(version=1, box_size=8, border=2)
    qr2.add_data("https://github.com/abhilok/krishiartha-mcp/releases/download/v1.0.0/KrishiArtha_MCP_Masterpiece_Demo.mp4")
    qr2.make(fit=True)
    img_qr2 = qr2.make_image(fill_color="#0f172a", back_color="#ffffff").convert("RGBA")

    # Card 1 (Left - Prototype)
    c1_x0, c1_y0 = 35, 35
    c1_x1, c1_y1 = 575, h - 35
    draw.rounded_rectangle([c1_x0, c1_y0, c1_x1, c1_y1], radius=18, fill=(16, 36, 45, 255), outline=(16, 185, 129, 255), width=2)
    
    # Place QR1
    qr1_size = 230
    img_qr1_resized = img_qr1.resize((qr1_size, qr1_size), Image.Resampling.LANCZOS)
    img.paste(img_qr1_resized, (c1_x0 + 25, c1_y0 + 110))

    # Text for Card 1
    draw.text((c1_x0 + 25, c1_y0 + 22), "QR CODE 1: LIVE PROTOTYPE", fill=(16, 185, 129, 255), font=get_font(18, bold=True))
    draw.text((c1_x0 + 25, c1_y0 + 50), "https://krishiartha-mcp.streamlit.app", fill=(56, 189, 248, 255), font=get_font(15, bold=True))
    draw.text((c1_x0 + 25, c1_y0 + 74), "Deployed on Streamlit Cloud • 100% Active APIs", fill=(148, 163, 184, 255), font=get_font(13))

    desc1_x = c1_x0 + 275
    draw.text((desc1_x, c1_y0 + 115), "📱 Instant Mobile Scan", fill=(248, 250, 252, 255), font=get_font(16, bold=True))
    draw.text((desc1_x, c1_y0 + 145), "• Zero app installation required", fill=(203, 213, 225, 255), font=get_font(13.5))
    draw.text((desc1_x, c1_y0 + 175), "• Works directly in mobile browser", fill=(203, 213, 225, 255), font=get_font(13.5))
    draw.text((desc1_x, c1_y0 + 205), "• Live Agmarknet + Weather data", fill=(203, 213, 225, 255), font=get_font(13.5))
    draw.text((desc1_x, c1_y0 + 235), "• Real-time Bhashini voice synthesis", fill=(203, 213, 225, 255), font=get_font(13.5))
    draw.text((desc1_x, c1_y0 + 265), "• 1-Click e-NWR Playwright filing", fill=(203, 213, 225, 255), font=get_font(13.5))

    draw.rounded_rectangle([desc1_x, c1_y0 + 305, c1_x1 - 25, c1_y0 + 342], radius=8, fill=(16, 185, 129, 40), outline=(16, 185, 129, 180), width=1)
    draw.text((desc1_x + 12, c1_y0 + 314), "✓ Cloud Verified & Running Live", fill=(52, 211, 153, 255), font=get_font(13, bold=True))

    # Card 2 (Right - Demo Video)
    c2_x0, c2_y0 = 625, 35
    c2_x1, c2_y1 = w - 35, h - 35
    draw.rounded_rectangle([c2_x0, c2_y0, c2_x1, c2_y1], radius=18, fill=(20, 32, 54, 255), outline=(56, 189, 248, 255), width=2)

    # Place QR2
    img_qr2_resized = img_qr2.resize((qr1_size, qr1_size), Image.Resampling.LANCZOS)
    img.paste(img_qr2_resized, (c2_x0 + 25, c2_y0 + 110))

    # Text for Card 2
    draw.text((c2_x0 + 25, c2_y0 + 22), "QR CODE 2: MASTERPIECE DEMO", fill=(56, 189, 248, 255), font=get_font(18, bold=True))
    draw.text((c2_x0 + 25, c2_y0 + 50), "Direct GitHub Release MP4 (5-Min HD)", fill=(245, 158, 11, 255), font=get_font(15, bold=True))
    draw.text((c2_x0 + 25, c2_y0 + 74), "1080p High-Bitrate Walkthrough with Full Narration", fill=(148, 163, 184, 255), font=get_font(13))

    desc2_x = c2_x0 + 275
    draw.text((desc2_x, c2_y0 + 115), "🎥 Failsafe Stage Video", fill=(248, 250, 252, 255), font=get_font(16, bold=True))
    draw.text((desc2_x, c2_y0 + 145), "• Exhaustive 5-minute video proof", fill=(203, 213, 225, 255), font=get_font(13.5))
    draw.text((desc2_x, c2_y0 + 175), "• Zero Wi-Fi dependence on stage", fill=(203, 213, 225, 255), font=get_font(13.5))
    draw.text((desc2_x, c2_y0 + 205), "• Audio narration in Marathi & English", fill=(203, 213, 225, 255), font=get_font(13.5))
    draw.text((desc2_x, c2_y0 + 235), "• 1.21s Playwright agent live capture", fill=(203, 213, 225, 255), font=get_font(13.5))
    draw.text((desc2_x, c2_y0 + 265), "• Complete 3-Column matrix proof", fill=(203, 213, 225, 255), font=get_font(13.5))

    draw.rounded_rectangle([desc2_x, c2_y0 + 305, c2_x1 - 25, c2_y0 + 342], radius=8, fill=(56, 189, 248, 40), outline=(56, 189, 248, 180), width=1)
    draw.text((desc2_x + 12, c2_y0 + 314), "✓ 1080p Masterpiece MP4 Ready", fill=(125, 211, 252, 255), font=get_font(13, bold=True))

    out_path = ASSETS_DIR / "dual_qr_evaluation.png"
    img.save(out_path, dpi=(300, 300))
    print(f"[OK] Generated {out_path} ({w}x{h})")

if __name__ == "__main__":
    generate_whatsapp_vernacular_card()
    generate_national_dpi_architecture()
    generate_security_shield_badges()
    generate_dual_qr_evaluation()
