"""
Generates the World-Class, Hackathon-Winning 9-Slide Pitch Deck in PowerPoint (.pptx)
for KrishiArtha-MCP (MandiPulse) — FORGE'26 GenAI Buildathon.

Features:
- Native PowerPoint Morph Transitions (<p15:morph option="byObject"/>)
- Deep Obsidian & Dark Slate Theme (#0F172A / #1E293B)
- High-contrast Emerald (#10B981), Amber (#F59E0B), Sky Blue (#38BDF8), Purple (#A855F7)
- 3D Photorealistic Agritech Hero Render
- 6 High-DPI Charts & UI Mockups (Chronos-2 fan chart, Arrhenius Q10 rot curve, LangGraph flow, WDRA slip, Browser UI, QR code)
- 3-Column Arbitrage Financial Table (+52% Net Surge)
- Judge Evaluation Verification Hub with live prototype link & QR code
"""

import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
OUTPUT_PATH = DOCS_DIR / "KrishiArtha_MCP_Pitch_Deck.pptx"
BACKUP_PATH = DOCS_DIR / "KrishiArtha_World_Class_Winning_Deck.pptx"

# ----------------- DESIGN TOKENS -----------------
DARK_BG      = RGBColor(15, 23, 42)       # Slate 900
CARD_BG      = RGBColor(30, 41, 59)       # Slate 800
CARD_BORDER  = RGBColor(51, 65, 85)       # Slate 700
EMERALD      = RGBColor(16, 185, 129)     # Emerald 500
EMERALD_BG   = RGBColor(6, 78, 59)        # Emerald 900
AMBER        = RGBColor(245, 158, 11)      # Amber 500
AMBER_BG     = RGBColor(120, 53, 15)      # Amber 900
SKY_BLUE     = RGBColor(56, 189, 248)     # Sky 400
PURPLE       = RGBColor(168, 85, 247)     # Purple 500
CRIMSON      = RGBColor(239, 68, 68)      # Red 500
TEXT_WHITE   = RGBColor(248, 250, 252)    # Slate 50
TEXT_MUTED   = RGBColor(148, 163, 184)    # Slate 400
TEXT_SUB     = RGBColor(203, 213, 225)    # Slate 300

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def apply_morph_transition(slide):
    """Injects native PowerPoint Morph transition into the slide XML."""
    try:
        transition_xml = parse_xml(
            '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            'xmlns:p15="http://schemas.microsoft.com/office/powerpoint/2012/main">'
            '<p15:morph option="byObject"/>'
            '</p:transition>'
        )
        slide._element.append(transition_xml)
    except Exception as e:
        print(f"[WARN] Could not inject morph transition: {e}")

def create_background(slide):
    """Creates a deep obsidian background rectangle."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = DARK_BG
    bg.line.fill.background()
    return bg

def add_header(slide, title, category="FORGE'26 HACKATHON • THEME B: CLIMATE & SUPPLY RESILIENCE", accent_color=EMERALD):
    """Renders a standard top header with category pill and bold title."""
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(10.5)
    p_c.font.bold = True
    p_c.font.color.rgb = accent_color

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

def add_card(slide, left, top, width, height, title, bullets, accent_color=EMERALD, title_size=15, bullet_size=11):
    """Draws a rounded glassmorphism style card container with bullet points."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    card.line.width = Pt(1.2)

    tb = slide.shapes.add_textbox(left + Inches(0.22), top + Inches(0.2), width - Inches(0.44), height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(title_size)
    p0.font.bold = True
    p0.font.color.rgb = accent_color
    p0.space_after = Pt(8)

    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(bullet_size)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(5)

    return card

# ==============================================================================
# SLIDE 1: Title & Vision Hero (With 3D Photorealistic Agritech Render)
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
create_background(s1)
apply_morph_transition(s1)

# Category Tag
cat_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(6.8), Inches(0.32))
tf = cat_box.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
tf.paragraphs[0].text = "FORGE'26 HACKATHON BUILD • THEME B: CLIMATE & SUPPLY RESILIENCE"
tf.paragraphs[0].font.size = Pt(10.5)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = EMERALD

# Prominent Live Prototype Badge
badge_bg = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.85), Inches(5.6), Inches(0.36))
badge_bg.fill.solid()
badge_bg.fill.fore_color.rgb = RGBColor(6, 78, 59)  # Deep Emerald
badge_bg.line.color.rgb = EMERALD
badge_bg.line.width = Pt(1.5)
tb_badge = s1.shapes.add_textbox(Inches(0.9), Inches(0.88), Inches(5.4), Inches(0.3))
tf_b = tb_badge.text_frame
tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
p_b = tf_b.paragraphs[0]
p_b.text = "● 100% Live Prototype Active on Streamlit Community Cloud"
p_b.font.size = Pt(10)
p_b.font.bold = True
p_b.font.color.rgb = RGBColor(167, 243, 208)  # Emerald 200

# Title & Crisp 8-Word YC One-Liner Subtitle
title_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(6.8), Inches(1.05))
tf = title_box.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "KrishiArtha-MCP"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE

p_sub = tf.add_paragraph()
p_sub.text = "Autonomous Climate Mandi Arbitrage & Statutory Distress-Credit Engine"
p_sub.font.size = Pt(13)
p_sub.font.bold = True
p_sub.font.color.rgb = SKY_BLUE
p_sub.space_before = Pt(4)

# Team Box
team_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.42), Inches(6.8), Inches(0.35))
tf = team_box.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p_team = tf.paragraphs[0]
p_team.text = "Team INFINITE LOOP (IIIT Guwahati) • Abhilok Reddy Bellamkonda & Sai Chandra"
p_team.font.size = Pt(11)
p_team.font.bold = True
p_team.font.color.rgb = TEXT_MUTED

# Two Bold Value Bullets Replacing Dense Text Block
val_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.82), Inches(6.8), Inches(1.4))
tf_v = val_box.text_frame
tf_v.word_wrap = True
tf_v.margin_left = tf_v.margin_right = tf_v.margin_top = tf_v.margin_bottom = 0

pv1 = tf_v.paragraphs[0]
pv1.space_after = Pt(8)
r1_lead = pv1.add_run()
r1_lead.text = "• The Crisis: "
r1_lead.font.bold = True
r1_lead.font.size = Pt(11.5)
r1_lead.font.color.rgb = AMBER
r1_text = pv1.add_run()
r1_text.text = "Halting ₹40,000+ Cr annual post-harvest distress sales triggered by unseasonal weather gluts."
r1_text.font.size = Pt(11.5)
r1_text.font.color.rgb = TEXT_SUB

pv2 = tf_v.add_paragraph()
r2_lead = pv2.add_run()
r2_lead.text = "• The Breakthrough: "
r2_lead.font.bold = True
r2_lead.font.size = Pt(11.5)
r2_lead.font.color.rgb = EMERALD
r2_text = pv2.add_run()
r2_text.text = "Fusing amazon/chronos-2 foundation AI, Arrhenius transit thermodynamics, and statutory NABARD e-NWR pledge liquidity."
r2_text.font.size = Pt(11.5)
r2_text.font.color.rgb = TEXT_SUB

# 4 Bento Stat Cards with Micro-Category Tags
bento_stats = [
    ("[CRISIS TARGET]", "₹40,000+ Cr", "Annual Post-Harvest Loss Targeted", AMBER),
    ("[VALIDATED GAIN]", "+52.0%", "Farmer Net Income Surge (Nashik 50qtl)", EMERALD),
    ("[1.21s SLA]", "1.21s", "Playwright WDRA Auto-Filing (<4.0s SLA)", SKY_BLUE),
    ("[70/70 TESTS]", "70/70", "Pytest Suite & AgentShield Grade A", PURPLE)
]
for idx, (tag, stat, label, col) in enumerate(bento_stats):
    b_left = Inches(0.8 + idx * 1.7)
    b_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, b_left, Inches(4.35), Inches(1.58), Inches(2.45))
    b_card.fill.solid()
    b_card.fill.fore_color.rgb = CARD_BG
    b_card.line.color.rgb = CARD_BORDER
    b_card.line.width = Pt(1.2)

    tb_stat = s1.shapes.add_textbox(b_left + Inches(0.1), Inches(4.45), Inches(1.38), Inches(2.25))
    tf_s = tb_stat.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0

    p_tag = tf_s.paragraphs[0]
    p_tag.text = tag
    p_tag.font.size = Pt(8)
    p_tag.font.bold = True
    p_tag.font.color.rgb = col
    p_tag.space_after = Pt(4)

    p_val = tf_s.add_paragraph()
    p_val.text = stat
    p_val.font.size = Pt(17)
    p_val.font.bold = True
    p_val.font.color.rgb = col
    p_val.space_after = Pt(6)

    p_lbl = tf_s.add_paragraph()
    p_lbl.text = label
    p_lbl.font.size = Pt(9.5)
    p_lbl.font.color.rgb = TEXT_MUTED

# Right Side: 3D Photorealistic Agritech Hero Image Frame
hero_img_path = ASSETS_DIR / "3d_hero_agritech.jpg"
if not hero_img_path.exists():
    hero_img_path = ASSETS_DIR / "agritech_pitch_deck_hero.jpg"
if hero_img_path.exists():
    frame = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(0.6), Inches(4.7), Inches(6.2))
    frame.fill.solid()
    frame.fill.fore_color.rgb = CARD_BG
    frame.line.color.rgb = EMERALD
    frame.line.width = Pt(2.0)

    s1.shapes.add_picture(str(hero_img_path), Inches(7.95), Inches(0.75), Inches(4.4), Inches(5.35))
    
    cap_box = s1.shapes.add_textbox(Inches(7.95), Inches(6.2), Inches(4.4), Inches(0.45))
    tf_cap = cap_box.text_frame
    tf_cap.word_wrap = True
    p_cap = tf_cap.paragraphs[0]
    p_cap.text = "AI + Physics + Statutory Liquidity Infrastructure"
    p_cap.font.size = Pt(10)
    p_cap.font.bold = True
    p_cap.font.color.rgb = EMERALD
    p_cap.alignment = PP_ALIGN.CENTER

# ==============================================================================
# SLIDE 2: Urgent Crisis & Smallholder Reality
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
create_background(s2)
apply_morph_transition(s2)
add_header(s2, "The Crisis: Why Existing Agri Systems Fail Smallholder Farmers",
           category="THE PROBLEM • GROUND REALITY CASE STUDY: FARMER RAMESH (NASHIK, 50 QTL TOMATOES)")

# Visual Diagram at Top: Causal Distress Cycle Flow
distress_img_path = ASSETS_DIR / "causal_distress_cycle.png"
if distress_img_path.exists():
    s2.shapes.add_picture(str(distress_img_path), Inches(0.8), Inches(1.28), Inches(11.733), Inches(2.25))

# 3 Bento Cards Below Diagram (Max 3 bullets each with bold colored lead-ins)
def add_card_with_lead_ins(slide, left, top, width, height, title, tag, items, accent_color):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = accent_color
    card.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p0 = tf.paragraphs[0]
    r_tag = p0.add_run()
    r_tag.text = f"{tag}\n"
    r_tag.font.size = Pt(8.5)
    r_tag.font.bold = True
    r_tag.font.color.rgb = accent_color
    
    r_tit = p0.add_run()
    r_tit.text = title
    r_tit.font.size = Pt(13.5)
    r_tit.font.bold = True
    r_tit.font.color.rgb = TEXT_WHITE
    p0.space_after = Pt(6)

    for lead, body in items:
        p = tf.add_paragraph()
        r_bullet = p.add_run()
        r_bullet.text = "• "
        r_bullet.font.size = Pt(9.5)
        r_bullet.font.bold = True
        r_bullet.font.color.rgb = accent_color

        r_lead = p.add_run()
        r_lead.text = lead + " "
        r_lead.font.size = Pt(9.5)
        r_lead.font.bold = True
        r_lead.font.color.rgb = accent_color

        r_body = p.add_run()
        r_body.text = body
        r_body.font.size = Pt(9.2)
        r_body.font.color.rgb = TEXT_SUB
        p.space_after = Pt(4)

    return card

card1_items = [
    ("Blind Telemetry:", "Agmarknet & eNAM only report yesterday's clearing price with zero forecast horizon."),
    ("Panic Stripping:", "Farmers harvest prematurely to avoid fungal mold, glutting mandis simultaneously."),
    ("Mandi Crash:", "Pimpalgaon APMC crashes to ₹900/qtl, collapsing deep below the ₹1,100 cost floor.")
]
add_card_with_lead_ins(s2, Inches(0.8), Inches(3.65), Inches(3.7), Inches(2.45),
                       "1. Passive & Backward-Looking", "[MARKET RIGIDITY]", card1_items, AMBER)

card2_items = [
    ("Spatial Trap:", "Portals recommend Surat APMC (234 km) @ ₹1,350/qtl assuming 0% transit decay."),
    ("Thermodynamic Rot:", "32°C & 85% RH triggers 18.4% microbial rot decay (-₹12,420 loss on 50 qtl lot)."),
    ("Freight Burden:", "₹6,800 diesel + handling collapses net arbitrage into a dangerous false trap (+7.3%).")
]
add_card_with_lead_ins(s2, Inches(4.81), Inches(3.65), Inches(3.7), Inches(2.45),
                       "2. Blind to Transit Rot & Diesel", "[THE TRANSIT MIRAGE]", card2_items, CRIMSON)

card3_items = [
    ("Predatory Debt:", "When mandis crash regionally, smallholders borrow from local lenders at 24%–36% APR."),
    ("Hidden Safety Net:", "Statutory NABARD Cir 128 / WDRA pledge financing remains completely undiscovered."),
    ("KrishiArtha Recourse:", "Instant 75% e-NWR pledge advance (₹33,750 @ 4% net interest) unlocks +52% rebound.")
]
add_card_with_lead_ins(s2, Inches(8.83), Inches(3.65), Inches(3.7), Inches(2.45),
                       "3. Zero Financial Safety Net", "[STATUTORY LIQUIDITY]", card3_items, EMERALD)

# Spatial Dilemma Callout Bar at Bottom
dilemma_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.22), Inches(11.733), Inches(0.9))
dilemma_box.fill.solid()
dilemma_box.fill.fore_color.rgb = CARD_BG
dilemma_box.line.color.rgb = AMBER
dilemma_box.line.width = Pt(1.5)

tb_dil = s2.shapes.add_textbox(Inches(0.95), Inches(6.27), Inches(11.433), Inches(0.8))
tf_d = tb_dil.text_frame
tf_d.word_wrap = True
tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0

pd1 = tf_d.paragraphs[0]
r_dil_head = pd1.add_run()
r_dil_head.text = "⚡ THE SPATIAL DILEMMA: "
r_dil_head.font.size = Pt(10.5)
r_dil_head.font.bold = True
r_dil_head.font.color.rgb = AMBER

r_dil1 = pd1.add_run()
r_dil1.text = "Pimpalgaon APMC (12 km) = ₹900/qtl Distress Crash (-₹10,000 Loss)   VS.   Surat APMC (234 km) = 18.4% Rot Trap (-₹12,420 Rot Loss + ₹6,800 Diesel = False Mirage)\n"
r_dil1.font.size = Pt(9.8)
r_dil1.font.color.rgb = TEXT_WHITE

r_sol_head = pd1.add_run()
r_sol_head.text = "🏆 KRISHIARTHA BREAKTHROUGH: "
r_sol_head.font.size = Pt(10.5)
r_sol_head.font.bold = True
r_sol_head.font.color.rgb = EMERALD

r_sol1 = pd1.add_run()
r_sol1.text = "MSWC Ozar (14.2 km) → ₹33,750 Immediate Cash Advance (75% LTV @ 4% KCC) + Day +10 Rebound → +₹23,400 Cash (+52.0% Income Surge)"
r_sol1.font.size = Pt(9.8)
r_sol1.font.bold = True
r_sol1.font.color.rgb = RGBColor(167, 243, 208)

# ==============================================================================
# SLIDE 3: Neuro-Symbolic Multi-Agent Architecture
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
create_background(s3)
apply_morph_transition(s3)
add_header(s3, "The Solution: 4-Node LangGraph Neuro-Symbolic State Machine",
           category="NEURO-SYMBOLIC ARCHITECTURE • ZERO LLM MATH HALLUCINATIONS • TYPED PYDANTIC V2 SCHEMAS")

# Subtitle / Latency Pill
sub_tb3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.18), Inches(11.733), Inches(0.3))
tf3_sub = sub_tb3.text_frame
tf3_sub.word_wrap = True
tf3_sub.margin_left = tf3_sub.margin_right = tf3_sub.margin_top = tf3_sub.margin_bottom = 0
p3_sub = tf3_sub.paragraphs[0]
p3_sub.text = "End-to-End Execution Latency: 1.04s (Target SLA: <4.0s) • Immutable Pydantic v2 State Contracts Prevent Schema Corruption"
p3_sub.font.size = Pt(10.5)
p3_sub.font.bold = True
p3_sub.font.color.rgb = SKY_BLUE

# Embed Upgraded Architecture Flow Chart
arch_img_path = ASSETS_DIR / "architecture_flow.png"
if arch_img_path.exists():
    s3.shapes.add_picture(str(arch_img_path), Inches(0.8), Inches(1.48), Inches(11.733), Inches(2.6))

# 4 Redesigned Bento Cards with Latency SLAs and Pydantic v2 Schemas
def add_sla_card(slide, left, top, width, height, title, sla_badge, schema_tag, items, accent_color):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = accent_color
    card.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(left + Inches(0.16), top + Inches(0.14), width - Inches(0.32), height - Inches(0.28))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p0 = tf.paragraphs[0]
    r_tit = p0.add_run()
    r_tit.text = f"{title}\n"
    r_tit.font.size = Pt(11.5)
    r_tit.font.bold = True
    r_tit.font.color.rgb = accent_color

    r_sla = p0.add_run()
    r_sla.text = f"[{sla_badge}]\n"
    r_sla.font.size = Pt(8.5)
    r_sla.font.bold = True
    r_sla.font.color.rgb = accent_color

    r_sch = p0.add_run()
    r_sch.text = f"Schema: {schema_tag}"
    r_sch.font.size = Pt(8.0)
    r_sch.font.bold = True
    r_sch.font.color.rgb = TEXT_MUTED
    p0.space_after = Pt(6)

    for lead, body in items:
        p = tf.add_paragraph()
        r_bullet = p.add_run()
        r_bullet.text = "• "
        r_bullet.font.size = Pt(9.2)
        r_bullet.font.bold = True
        r_bullet.font.color.rgb = accent_color

        r_lead = p.add_run()
        r_lead.text = lead + " "
        r_lead.font.size = Pt(9.2)
        r_lead.font.bold = True
        r_lead.font.color.rgb = accent_color

        r_body = p.add_run()
        r_body.text = body
        r_body.font.size = Pt(8.8)
        r_body.font.color.rgb = TEXT_SUB
        p.space_after = Pt(3)

    return card

node1_items = [
    ("Live Telemetry:", "Zero mock data; pulls Agmarknet OGD API (9ef84268...) + Open-Meteo 7-day hourly rain/temp."),
    ("OSRM Routing:", "Computes exact highway distances & transit hours via router.project-osrm.org."),
    ("State Contract:", "Inputs validated into immutable Pydantic v2 contract preventing injection.")
]
add_sla_card(s3, Inches(0.8), Inches(4.2), Inches(2.78), Inches(2.95),
             "Node 1: FastMCP Ingest", "410ms SLA", "MandiTelemetryPayload", node1_items, SKY_BLUE)

node2_items = [
    ("Foundation AI:", "amazon/chronos-2 zero-shot model conditioned on rainfall & temp covariates."),
    ("Price Quantiles:", "Emits P10, P50, P90 trajectories; pins Day +10 rebound to ₹1,480/qtl (+64.4%)."),
    ("Deterministic:", "Numeric time-series tensors eliminate generative LLM pricing hallucinations.")
]
add_sla_card(s3, Inches(3.78), Inches(4.2), Inches(2.78), Inches(2.95),
             "Node 2: Chronos-2", "280ms SLA", "PriceForecastDistribution", node2_items, EMERALD)

node3_items = [
    ("Arrhenius Q10:", "Thermodynamic rot decay (Q10=2.2, 18.4% decay) + 2.5h APMC unloading buffer."),
    ("Diesel Freight:", "Round-trip mini-truck (₹22/km) + ₹35/qtl handling -> Net Realizable Price (NRP)."),
    ("Symbolic Integrity:", "Deterministic physics kernel prevents fake long-distance arbitrage traps.")
]
add_sla_card(s3, Inches(6.76), Inches(4.2), Inches(2.78), Inches(2.95),
             "Node 3: Spoilage Physics", "12ms SLA", "ArbitrageRanking", node3_items, AMBER)

node4_items = [
    ("Policy Graph:", "LightRAG hybrid graph indexes NABARD Circular 128 (75% LTV @ 4% net interest)."),
    ("interrupt() Gate:", "LangGraph stateful barrier halts execution for explicit farmer consent."),
    ("Browser Agent:", "Playwright agent auto-fills WDRA portal & emits sanction slip in 1.21s.")
]
add_sla_card(s3, Inches(9.74), Inches(4.2), Inches(2.78), Inches(2.95),
             "Node 4: LightRAG & Consent", "340ms SLA", "SanctionExecutionRecord", node4_items, PURPLE)

# ==============================================================================
# SLIDE 4: Scientific & Mathematical Defensibility
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
create_background(s4)
apply_morph_transition(s4)
add_header(s4, "Scientific & Mathematical Rigor: Zero Hallucinated Math")

# Left Column: Arrhenius Q10 Physics
card_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.0))
card_l.fill.solid()
card_l.fill.fore_color.rgb = CARD_BG
card_l.line.color.rgb = CARD_BORDER
card_l.line.width = Pt(1.2)

tb_l = s4.shapes.add_textbox(Inches(1.0), Inches(1.42), Inches(5.3), Inches(0.35))
tf_l = tb_l.text_frame
tf_l.word_wrap = True
p = tf_l.paragraphs[0]
p.text = "Arrhenius Q10 Biological Transit Rot Decay"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = EMERALD

annotated_spoilage_img = ASSETS_DIR / "annotated_arrhenius_rot.png"
if annotated_spoilage_img.exists():
    s4.shapes.add_picture(str(annotated_spoilage_img), Inches(1.0), Inches(1.82), Inches(5.3), Inches(2.65))

tb_math_l = s4.shapes.add_textbox(Inches(1.0), Inches(4.55), Inches(5.3), Inches(1.7))
tf_ml = tb_math_l.text_frame
tf_ml.word_wrap = True
bullets_l = [
    "Thermal Decay: k(T, RH) = k_base · (Q_10)^((T-20)/10) · [1 + α · max(0, (RH-70)/100)]",
    "Parameters (Tomato): k_base = 0.0065, Q_10 = 2.2, α = 1.5. Mandatory queue buffer = +2.5 hrs.",
    "Physical Spoilage Fraction: L = 1 - exp(-k · t_transit), where t_transit = t_road + 2.5h.",
    "Net Realizable Price: NRP_m = [P_50 · (1 - L) · (1 - γ_APMC)] - (C_transport / Q)"
]
for b in bullets_l:
    p = tf_ml.add_paragraph() if tf_ml.paragraphs[0].text else tf_ml.paragraphs[0]
    p.text = "• " + b
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(2.5)

# Right Column: Chronos-2 Foundation Forecaster
card_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.0))
card_r.fill.solid()
card_r.fill.fore_color.rgb = CARD_BG
card_r.line.color.rgb = CARD_BORDER
card_r.line.width = Pt(1.2)

tb_r = s4.shapes.add_textbox(Inches(7.0), Inches(1.42), Inches(5.3), Inches(0.35))
tf_r = tb_r.text_frame
tf_r.word_wrap = True
p = tf_r.paragraphs[0]
p.text = "amazon/chronos-2 Probabilistic Quantiles"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = SKY_BLUE

annotated_chronos_img = ASSETS_DIR / "annotated_chronos_rebound.png"
if annotated_chronos_img.exists():
    s4.shapes.add_picture(str(annotated_chronos_img), Inches(7.0), Inches(1.82), Inches(5.3), Inches(2.65))

tb_math_r = s4.shapes.add_textbox(Inches(7.0), Inches(4.55), Inches(5.3), Inches(1.7))
tf_mr = tb_math_r.text_frame
tf_mr.word_wrap = True
bullets_r = [
    "Zero-Shot T5 Architecture: Pretrained on billions of time-series tokens; zero hallucination.",
    "Covariate Ingestion: Integrates 7-day Open-Meteo precipitation & temperature tensors.",
    "Quantile Risk Bounds: P10, P50, P90 confidence intervals prevent overconfident suggestions.",
    "Post-Glut Rebound: Reliably projects Day +10 rebound to ₹1,480/qtl (+64.4% recovery surge)."
]
for b in bullets_r:
    p = tf_mr.add_paragraph() if tf_mr.paragraphs[0].text else tf_mr.paragraphs[0]
    p.text = "• " + b
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(2.5)

# Bottom LLM Contrast Banner
card_contrast = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.45), Inches(11.7), Inches(0.72))
card_contrast.fill.solid()
card_contrast.fill.fore_color.rgb = RGBColor(30, 20, 25)
card_contrast.line.color.rgb = CRIMSON
card_contrast.line.width = Pt(1.2)

tb_cont = s4.shapes.add_textbox(Inches(0.95), Inches(6.48), Inches(11.4), Inches(0.65))
tf_c = tb_cont.text_frame
tf_c.word_wrap = True
p_c1 = tf_c.paragraphs[0]
p_c1.text = "WHY GENERIC LLMs FAIL VS KRISHIARTHA DETERMINISTIC FOUNDATION SPINE:"
p_c1.font.size = Pt(9.5)
p_c1.font.bold = True
p_c1.font.color.rgb = CRIMSON

p_c2 = tf_c.add_paragraph()
p_c2.text = "Generic LLMs cannot compute non-linear exponential Arrhenius decay, hallucinate transit distances, and guess future prices. KrishiArtha decouples zero-shot foundation forecasting (amazon/chronos-2) from deterministic USDA/FAO Arrhenius decay kinetics and OSRM highway geometry — guaranteeing 100% mathematical defensibility."
p_c2.font.size = Pt(8.5)
p_c2.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 5: The 3-Column Arbitrage Matrix (Nashik 50 qtl Lot)
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
create_background(s5)
apply_morph_transition(s5)
add_header(s5, "The 3-Column Financial Arbitrage Matrix (Nashik 50 qtl Lot)")

sub_tb5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.7), Inches(0.35))
sub_tf5 = sub_tb5.text_frame
sub_p5 = sub_tf5.paragraphs[0]
sub_p5.text = "Mathematical Proof: How WDRA e-NWR Warehousing Beats Long-Distance Arbitrage by +52% Net"
sub_p5.font.size = Pt(12)
sub_p5.font.color.rgb = SKY_BLUE

# Left Table (8 Rows: 1 Header + 7 Data Rows including Row 5b)
table_shape = s5.shapes.add_table(8, 4, Inches(0.8), Inches(1.65), Inches(7.3), Inches(4.55))
tbl = table_shape.table

tbl.columns[0].width = Inches(2.05)
tbl.columns[1].width = Inches(1.7)
tbl.columns[2].width = Inches(1.75)
tbl.columns[3].width = Inches(1.8)

headers5 = [
    "Financial Metric",
    "The Local Distress Trap\n(Pimpalgaon APMC)",
    "The False Transit Mirage\n(Surat APMC)",
    "The KrishiArtha Breakthrough\n(MSWC Ozar WDRA)"
]
matrix_data5 = [
    ["Destination Mandi / Storage", "Pimpalgaon (12 km)", "Surat APMC (234 km)", "MSWC Cold Storage (14.2 km)"],
    ["Nominal Quoted Price", "₹900 / qtl (Severe Crash)", "₹1,350 / qtl (Apparent Arbitrage)", "Rebound: ₹1,480 / qtl (Day +10)"],
    ["Arrhenius Q10 Transit Rot", "₹945 (2.1% loss)", "₹12,420 (18.4% Thermal Rot!)", "₹0 (Cold Storage Preserved)"],
    ["Round-Trip Freight & Handling", "₹1,925 (Local mini-truck)", "₹6,800 (₹22/km Round-Trip)", "₹750 (Short warehouse haul)"],
    ["Immediate Farmer Liquidity", "₹45,000 (Immediate Cash)", "₹48,280 (Post-transit payout)", "₹33,750 (75% LTV @ 4% KCC Int.)"],
    ["Cold Storage & Subvented Interest", "₹0 (No storage)", "₹0 (Direct sale)", "-₹5,600 (₹4.2k Cold + ₹1.4k KCC Int.)"],
    ["Final Net Realization", "₹45,000 Net Baseline", "₹48,280 Net (+7.3% False Trap)", "₹68,400 Net (+52.0% Income Surge)"]
]

for col_idx, h in enumerate(headers5):
    cell = tbl.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = CARD_BG
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = EMERALD if col_idx == 3 else TEXT_WHITE

for row_idx, row in enumerate(matrix_data5):
    for col_idx, val in enumerate(row):
        cell = tbl.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        if col_idx == 3:
            cell.fill.fore_color.rgb = EMERALD_BG if row_idx == 6 else RGBColor(10, 50, 40)
        else:
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 0 else RGBColor(20, 30, 48)
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(8.5)
        if col_idx == 3 or row_idx == 6:
            p.font.bold = True
            p.font.color.rgb = EMERALD if col_idx == 3 else TEXT_WHITE
        else:
            p.font.color.rgb = TEXT_WHITE

# Right Side: Visual 3-Bar Comparison Chart
bar_chart_path = ASSETS_DIR / "financial_arbitrage_3bar.png"
if bar_chart_path.exists():
    s5.shapes.add_picture(str(bar_chart_path), Inches(8.25), Inches(1.65), Inches(4.28), Inches(4.55))

# Bottom Banner Callout
bot_banner = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.32), Inches(11.73), Inches(0.85))
bot_banner.fill.solid()
bot_banner.fill.fore_color.rgb = CARD_BG
bot_banner.line.color.rgb = EMERALD
bot_banner.line.width = Pt(1.5)

tf_bb = bot_banner.text_frame
tf_bb.word_wrap = True
p_bb = tf_bb.paragraphs[0]
p_bb.text = "VERIFIED IMPACT: Option C delivers +₹23,400 (+52.0%) higher net income than local distress selling, while releasing ₹33,750 immediate liquidity on Day 0 via statutory NABARD e-NWR pledge financing. Deduction itemized: ₹74,000 gross - ₹5,600 (storage & subvented interest) = ₹68,400 net."
p_bb.font.size = Pt(10.5)
p_bb.font.bold = True
p_bb.font.color.rgb = EMERALD
p_bb.alignment = PP_ALIGN.CENTER

# ==============================================================================
# SLIDE 6: Human-in-the-Loop Governance & Playwright Browser Agent
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
create_background(s6)
apply_morph_transition(s6)
add_header(s6, "Autonomous Execution & Human Governance")

sub_tb6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.7), Inches(0.35))
sub_tf6 = sub_tb6.text_frame
sub_p6 = sub_tf6.paragraphs[0]
sub_p6.text = "LangGraph interrupt() consent barrier + automated Playwright WDRA filing agent (<1.5s SLA)"
sub_p6.font.size = Pt(12)
sub_p6.font.color.rgb = SKY_BLUE

# Top: 3-step LangGraph State Machine visual sequence
flow_img_path = ASSETS_DIR / "langgraph_governance_flow.png"
if flow_img_path.exists():
    s6.shapes.add_picture(str(flow_img_path), Inches(0.8), Inches(1.65), Inches(11.73), Inches(2.45))

# Bottom Left: Governance Guardrails Card
add_card(s6, Inches(0.8), Inches(4.25), Inches(5.6), Inches(2.9),
         "LangGraph interrupt() & Governance Safeguards",
         [
             "Zero Autonomous Execution: interrupt() unconditionally halts state before warehouse lock or bank pledge.",
             "Vernacular Consent Dispatch: Farmer receives exact 3-column financial comparison in Marathi/Hindi via WhatsApp/IVR.",
             "Cryptographic Audit Trail: Only resumes upon human Command(resume=True), logging timestamped hash #78a2f1 to Postgres.",
             "700x Speedup: Playwright agent executes in 1.21s (SLA <4.0s) vs 15-20 minutes manual human portal navigation."
         ], EMERALD, title_size=13, bullet_size=9.5)

# Bottom Right: Annotated WDRA Sanction Slip with Callouts
annotated_slip_path = ASSETS_DIR / "annotated_wdra_sanction.png"
if annotated_slip_path.exists():
    frame_s = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.6), Inches(4.25), Inches(5.93), Inches(2.9))
    frame_s.fill.solid()
    frame_s.fill.fore_color.rgb = CARD_BG
    frame_s.line.color.rgb = EMERALD
    frame_s.line.width = Pt(1.5)

    s6.shapes.add_picture(str(annotated_slip_path), Inches(6.75), Inches(4.35), Inches(5.63), Inches(2.7))

# ==============================================================================
# SLIDE 7: Vernacular Edge Experience & Dual-Device Multi-Modal Interface
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
create_background(s7)
apply_morph_transition(s7)
add_header(s7, "Edge & Vernacular Experience: Dual-Device Multi-Modal Interface")

sub_tb7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.28), Inches(11.7), Inches(0.32))
sub_tf7 = sub_tb7.text_frame
sub_p7 = sub_tf7.paragraphs[0]
sub_p7.text = "Desktop Mission Control Cockpit (FPO/Trader) paired with Smartphone WhatsApp Voice Note Rails (Smallholder Farmer)"
sub_p7.font.size = Pt(11.5)
sub_p7.font.color.rgb = SKY_BLUE

# Left Side: Desktop Mission Control Cockpit (Streamlit UI)
frame_ui = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.62), Inches(6.45), Inches(4.75))
frame_ui.fill.solid()
frame_ui.fill.fore_color.rgb = CARD_BG
frame_ui.line.color.rgb = SKY_BLUE
frame_ui.line.width = Pt(1.5)

ui_mockup_path = ASSETS_DIR / "browser_mockup.png"
if ui_mockup_path.exists():
    s7.shapes.add_picture(str(ui_mockup_path), Inches(0.95), Inches(1.75), Inches(6.15), Inches(3.6))

tb_ui_cap = s7.shapes.add_textbox(Inches(0.95), Inches(5.4), Inches(6.15), Inches(0.9))
tf_uic = tb_ui_cap.text_frame
tf_uic.word_wrap = True
p = tf_uic.paragraphs[0]
p.text = "FPO & Mandi Trader View: Streamlit Mission Control Cockpit"
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = SKY_BLUE

p2 = tf_uic.add_paragraph()
p2.text = "Live Agmarknet prices, real-time Open-Meteo storm radar, Arrhenius rot alerts & 1-click WDRA filing.\n🌐 Live Web Prototype: https://krishiartha-mcp.streamlit.app"
p2.font.size = Pt(9.2)
p2.font.color.rgb = TEXT_WHITE
p2.space_before = Pt(2)

# Right Side: Smartphone Vernacular WhatsApp Voice Note Card in Marathi
frame_wa = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.45), Inches(1.62), Inches(5.08), Inches(4.75))
frame_wa.fill.solid()
frame_wa.fill.fore_color.rgb = CARD_BG
frame_wa.line.color.rgb = EMERALD
frame_wa.line.width = Pt(1.5)

wa_card_path = ASSETS_DIR / "whatsapp_vernacular_card.png"
if wa_card_path.exists():
    s7.shapes.add_picture(str(wa_card_path), Inches(7.58), Inches(1.72), Inches(4.82), Inches(4.55))

# Footer Trust & Speech Rails Banner
ft_banner = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.48), Inches(11.73), Inches(0.58))
ft_banner.fill.solid()
ft_banner.fill.fore_color.rgb = CARD_BG
ft_banner.line.color.rgb = CARD_BORDER
ft_banner.line.width = Pt(1.0)

tf_ft = ft_banner.text_frame
tf_ft.word_wrap = True
p_ft = tf_ft.paragraphs[0]
p_ft.text = "🌐 Bhashini ULCA Multilingual Speech Rails: मराठी (Marathi) • हिन्दी (Hindi) • తెలుగు (Telugu) • English (22 Scheduled Languages)\n🛡️ Stage Certified: 100% Offline Safe-Mode Resilient (OFFLINE_STAGE_SAFE_MODE=true • Zero Stage Wi-Fi Risk)"
p_ft.font.size = Pt(9.8)
p_ft.font.bold = True
p_ft.font.color.rgb = EMERALD
p_ft.alignment = PP_ALIGN.CENTER

# ==============================================================================
# SLIDE 8: Enterprise Security, Verification & National DPI Scalability
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
create_background(s8)
apply_morph_transition(s8)
add_header(s8, "Enterprise Security Audit & National DPI Scalability")

sub_tb8 = s8.shapes.add_textbox(Inches(0.8), Inches(1.28), Inches(11.7), Inches(0.32))
sub_tf8 = sub_tb8.text_frame
sub_p8 = sub_tf8.paragraphs[0]
sub_p8.text = "AgentShield Grade A certified posture + Interconnected national agricultural digital public infrastructure"
sub_p8.font.size = Pt(11.5)
sub_p8.font.color.rgb = SKY_BLUE

# Top: 3 Security Shield Badges (De-textified graphic)
sec_badges_path = ASSETS_DIR / "security_shield_badges.png"
if sec_badges_path.exists():
    frame_sec = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.62), Inches(11.73), Inches(2.25))
    frame_sec.fill.solid()
    frame_sec.fill.fore_color.rgb = CARD_BG
    frame_sec.line.color.rgb = EMERALD
    frame_sec.line.width = Pt(1.2)
    s8.shapes.add_picture(str(sec_badges_path), Inches(0.85), Inches(1.66), Inches(11.63), Inches(2.17))

# Bottom: National DPI Architecture Interconnect Diagram
dpi_arch_path = ASSETS_DIR / "national_dpi_architecture.png"
if dpi_arch_path.exists():
    frame_dpi = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.98), Inches(11.73), Inches(3.15))
    frame_dpi.fill.solid()
    frame_dpi.fill.fore_color.rgb = CARD_BG
    frame_dpi.line.color.rgb = SKY_BLUE
    frame_dpi.line.width = Pt(1.2)
    s8.shapes.add_picture(str(dpi_arch_path), Inches(0.85), Inches(4.02), Inches(11.63), Inches(3.07))

# ==============================================================================
# SLIDE 9: Evaluation Hub & Rapid Verification Protocol
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
create_background(s9)
apply_morph_transition(s9)
add_header(s9, "Judge Evaluation Hub & Rapid Verification Protocol")

sub_tb9 = s9.shapes.add_textbox(Inches(0.8), Inches(1.28), Inches(11.7), Inches(0.32))
sub_tf9 = sub_tb9.text_frame
sub_p9 = sub_tf9.paragraphs[0]
sub_p9.text = "Zero-friction live verification for FORGE'26 evaluators • Dual QR codes for cloud prototype & 5-min HD demo"
sub_p9.font.size = Pt(11.5)
sub_p9.font.color.rgb = SKY_BLUE

# Left Side: 4-Step Rapid Test Vector Card
add_card(s9, Inches(0.8), Inches(1.62), Inches(5.9), Inches(4.4),
         "4-Step Rapid Evaluator Test Vector",
         [
             "1. Open Prototype (10s): Scan QR 1 or visit https://krishiartha-mcp.streamlit.app on any device.",
             "2. Input Test Vector (15s): Select District: Nashik | Crop: Tomato | Lot Size: 50 Quintals.",
             "3. Review Financial Matrix (20s): Observe Pimpalgaon ₹900 crash vs MSWC ₹1,480 rebound (+52.0% net gain).",
             "4. Trigger Execution (1.21s): Click 'Approve WDRA Filing (होय)' -> Observe Playwright auto-issue sanction slip.",
             "Codebase Verification: 70/70 Pytests Passing in 11.3s | OFFLINE_STAGE_SAFE_MODE=true air-gap certified."
         ], EMERALD, title_size=15, bullet_size=10.5)

# Right Side: Dual QR Code Asset
dual_qr_path = ASSETS_DIR / "dual_qr_evaluation.png"
if dual_qr_path.exists():
    frame_qr = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.62), Inches(5.63), Inches(4.4))
    frame_qr.fill.solid()
    frame_qr.fill.fore_color.rgb = CARD_BG
    frame_qr.line.color.rgb = SKY_BLUE
    frame_qr.line.width = Pt(1.5)
    s9.shapes.add_picture(str(dual_qr_path), Inches(7.0), Inches(1.75), Inches(5.43), Inches(4.14))

# Bottom Banner: The Winning Thesis
thesis_banner = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.14), Inches(11.73), Inches(0.95))
thesis_banner.fill.solid()
thesis_banner.fill.fore_color.rgb = CARD_BG
thesis_banner.line.color.rgb = EMERALD
thesis_banner.line.width = Pt(1.8)

tf_tb = thesis_banner.text_frame
tf_tb.word_wrap = True
p_tb1 = tf_tb.paragraphs[0]
p_tb1.text = "WINNING THESIS: KrishiArtha transforms unseasonal weather from a source of agrarian bankruptcy into a guaranteed driver of smallholder wealth."
p_tb1.font.size = Pt(12)
p_tb1.font.bold = True
p_tb1.font.color.rgb = EMERALD
p_tb1.alignment = PP_ALIGN.CENTER

p_tb2 = tf_tb.add_paragraph()
p_tb2.text = "Fusing foundation time-series forecasting, Arrhenius transit thermodynamics, and statutory pledge liquidity into India's agricultural DPI."
p_tb2.font.size = Pt(10)
p_tb2.font.color.rgb = SKY_BLUE
p_tb2.alignment = PP_ALIGN.CENTER
p_tb2.space_before = Pt(3)

# ----------------- SAVE PRESENTATION -----------------
prs.save(str(OUTPUT_PATH))
print(f"[OK] Saved World-Class Pitch Deck to: {OUTPUT_PATH}")

# Save backup copy
prs.save(str(BACKUP_PATH))
print(f"[OK] Saved Backup Pitch Deck to: {BACKUP_PATH}")
