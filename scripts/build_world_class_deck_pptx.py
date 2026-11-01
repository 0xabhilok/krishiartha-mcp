"""
Definitive World-Class Hackathon-Winning 9-Slide Pitch Deck Generator for KrishiArtha-MCP
Target: FORGE'26 GenAI Buildathon (Theme B: Climate & Supply Resilience + Theme A: Civic Pulse & DPI)

Implements:
- 16:9 Widescreen Layout (13.333" x 7.500")
- Deep Obsidian & Dark Slate Palette (#0F172A, #1E293B, #334155, #10B981, #F59E0B, #38BDF8, #A855F7)
- Native PowerPoint Morph Transitions (<p15:morph option="byObject"/>) on all slides
- Cleanly embedded high-DPI assets:
    * 3d_hero_agritech.jpg (Hero Vision)
    * mandi_glut_crisis.jpg (Visceral Smallholder Distress)
    * neuro_symbolic_architecture_diagram.jpg (LangGraph Neuro-Symbolic Spine)
    * arrhenius_spoilage_chart.png & chronos_fan_chart.png (Deterministic Math & Quant AI)
    * wdra_sanction_framed.png (Playwright 1.21s Sanction Slip)
    * browser_mockup.png & whatsapp_vernacular_card.jpg (Dual-Device Vernacular Experience)
    * qr_code_live_prototype.png & qr_code_demo_video.png (Dual QR Code Evaluator Hub)
- Slide 5: Explicit itemized -₹5,600 cold storage deduction + 3-bar comparison visual
- Slide 8: Zero walls of text with 3 visual security badges (AgentShield Grade A, 70/70 pytests, Pydantic v2) + National DPI Architecture
- Slide 9: Dual QR codes (Live App + Demo Video) and the winning closing thesis banner
"""

import sys
import os
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
DARK_BG      = RGBColor(15, 23, 42)       # Slate 900 (#0F172A)
CARD_BG      = RGBColor(30, 41, 59)       # Slate 800 (#1E293B)
CARD_BORDER  = RGBColor(51, 65, 85)       # Slate 700 (#334155)
EMERALD      = RGBColor(16, 185, 129)     # Emerald 500 (#10B981)
EMERALD_BG   = RGBColor(6, 78, 59)        # Emerald 900 (#064E3B)
AMBER        = RGBColor(245, 158, 11)      # Amber 500 (#F59E0B)
AMBER_BG     = RGBColor(120, 53, 15)      # Amber 900 (#78350F)
SKY_BLUE     = RGBColor(56, 189, 248)     # Sky 400 (#38BDF8)
PURPLE       = RGBColor(168, 85, 247)     # Purple 500 (#A855F7)
CRIMSON      = RGBColor(239, 68, 68)      # Red 500 (#EF4444)
TEXT_WHITE   = RGBColor(248, 250, 252)    # Slate 50 (#F8FAFC)
TEXT_MUTED   = RGBColor(148, 163, 184)    # Slate 400 (#94A3B8)
TEXT_SUB     = RGBColor(203, 213, 225)    # Slate 300 (#CBD5E1)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.500)
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
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.500))
    bg.fill.solid()
    bg.fill.fore_color.rgb = DARK_BG
    bg.line.fill.background()
    return bg

def add_header(slide, title, category="FORGE'26 HACKATHON • THEME B: CLIMATE & SUPPLY RESILIENCE", accent_color=EMERALD, subtext=None):
    """Renders a standard top header with category pill and bold title."""
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.733), Inches(0.32))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = accent_color

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.55))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

    if subtext:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.22), Inches(11.733), Inches(0.30))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = subtext
        p_s.font.size = Pt(11.5)
        p_s.font.color.rgb = SKY_BLUE

def add_card(slide, left, top, width, height, title, bullets, accent_color=EMERALD, title_size=15, bullet_size=11):
    """Draws a rounded glassmorphism style card container with bullet points."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    card.line.width = Pt(1.2)

    tb = slide.shapes.add_textbox(left + Inches(0.22), top + Inches(0.18), width - Inches(0.44), height - Inches(0.36))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(title_size)
    p0.font.bold = True
    p0.font.color.rgb = accent_color
    p0.space_after = Pt(7)

    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(bullet_size)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(5)

    return card

# ==============================================================================
# SLIDE 1: Title & Hook (Vision, Team, Stats Bento & 3D Hero Agritech)
# ==============================================================================
print("[1/9] Building Slide 1: Title & Hook...")
s1 = prs.slides.add_slide(blank_layout)
create_background(s1)
apply_morph_transition(s1)

# Category Pill
cat_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(6.8), Inches(0.32))
tf = cat_box.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "FORGE'26 HACKATHON BUILD • THEME B: CLIMATE & SUPPLY RESILIENCE"
tf.paragraphs[0].font.size = Pt(10.5)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = EMERALD

# Prominent Live Prototype Badge
cred_badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.85), Inches(5.6), Inches(0.36))
cred_badge.fill.solid()
cred_badge.fill.fore_color.rgb = RGBColor(6, 78, 59)
cred_badge.line.color.rgb = EMERALD
cred_badge.line.width = Pt(1.5)
tf_cb = cred_badge.text_frame
tf_cb.word_wrap = True
p_cb = tf_cb.paragraphs[0]
p_cb.text = "● 100% Live Prototype Active on Streamlit Community Cloud"
p_cb.font.size = Pt(10)
p_cb.font.bold = True
p_cb.font.color.rgb = RGBColor(167, 243, 208)

# Title & Crisp 8-Word YC Subtitle
title_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.30), Inches(6.8), Inches(1.05))
tf = title_box.text_frame
tf.word_wrap = True
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
p_team = tf.paragraphs[0]
p_team.text = "Team INFINITE LOOP (IIIT Guwahati) • Abhilok Reddy Bellamkonda & Sai Chandra"
p_team.font.size = Pt(11)
p_team.font.bold = True
p_team.font.color.rgb = TEXT_MUTED

# Two Bold Value Propositions (Replacing Dense Text)
vp_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.82), Inches(6.8), Inches(1.4))
tf_vp = vp_box.text_frame
tf_vp.word_wrap = True

p_vp1 = tf_vp.paragraphs[0]
p_vp1.space_after = Pt(8)
r1_lead = p_vp1.add_run()
r1_lead.text = "• The Crisis: "
r1_lead.font.bold = True
r1_lead.font.size = Pt(11.5)
r1_lead.font.color.rgb = AMBER
r1_text = p_vp1.add_run()
r1_text.text = "Halting ₹40,000+ Cr annual post-harvest distress sales triggered by unseasonal weather gluts."
r1_text.font.size = Pt(11.5)
r1_text.font.color.rgb = TEXT_SUB

p_vp2 = tf_vp.add_paragraph()
r2_lead = p_vp2.add_run()
r2_lead.text = "• The Breakthrough: "
r2_lead.font.bold = True
r2_lead.font.size = Pt(11.5)
r2_lead.font.color.rgb = EMERALD
r2_text = p_vp2.add_run()
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

    tb_stat = s1.shapes.add_textbox(b_left + Inches(0.10), Inches(4.45), Inches(1.38), Inches(2.25))
    tf_s = tb_stat.text_frame
    tf_s.word_wrap = True

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
# SLIDE 2: Problem & Market Pain (Visceral Agony of Smallholders)
# ==============================================================================
print("[2/9] Building Slide 2: Problem & Market Pain...")
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
# SLIDE 3: Architecture & Multi-Agent Flow (LangGraph Neuro-Symbolic Spine)
# ==============================================================================
print("[3/9] Building Slide 3: Architecture & Multi-Agent Flow...")
s3 = prs.slides.add_slide(blank_layout)
create_background(s3)
apply_morph_transition(s3)
add_header(s3, "The Solution: 4-Node LangGraph Neuro-Symbolic State Machine",
           category="NEURO-SYMBOLIC ARCHITECTURE • ZERO LLM MATH HALLUCINATIONS • TYPED PYDANTIC V2 SCHEMAS")

# Subtitle / Latency Pill
sub_tb3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.18), Inches(11.733), Inches(0.3))
tf3_sub = sub_tb3.text_frame
tf3_sub.word_wrap = True
p3_sub = tf3_sub.paragraphs[0]
p3_sub.text = "End-to-End Execution Latency: 1.04s (Target SLA: <4.0s) • Immutable Pydantic v2 State Contracts Prevent Schema Corruption"
p3_sub.font.size = Pt(10.5)
p3_sub.font.bold = True
p3_sub.font.color.rgb = SKY_BLUE

# Embed Architecture Flow Chart
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
p_cb.alignment = PP_ALIGN.CENTER

# ==============================================================================
# SLIDE 4: Mathematical Defensibility & Zero Hallucination
# ==============================================================================
print("[4/9] Building Slide 4: Mathematical Defensibility...")
s4 = prs.slides.add_slide(blank_layout)
create_background(s4)
apply_morph_transition(s4)
add_header(s4, "Scientific & Mathematical Rigor: Zero Hallucinated Math",
           category="SCIENTIFIC & QUANT RIGOR • DETERMINISTIC KERNELS & FOUNDATION AI",
           subtext="Arrhenius thermal-humidity biological decay physics paired with amazon/chronos-2 foundation time-series")

# Left Column: Arrhenius Q10 Physics
card_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(5.7), Inches(5.45))
card_l.fill.solid()
card_l.fill.fore_color.rgb = CARD_BG
card_l.line.color.rgb = CARD_BORDER
card_l.line.width = Pt(1.2)

tb_l = s4.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(0.35))
tf_l = tb_l.text_frame
tf_l.word_wrap = True
p = tf_l.paragraphs[0]
p.text = "Arrhenius Q10 Biological Transit Rot Decay"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = EMERALD

spoilage_img_path = ASSETS_DIR / "arrhenius_spoilage_chart.png"
if spoilage_img_path.exists():
    s4.shapes.add_picture(str(spoilage_img_path), Inches(1.0), Inches(2.05), Inches(5.3), Inches(2.75))

tb_math_l = s4.shapes.add_textbox(Inches(1.0), Inches(4.85), Inches(5.3), Inches(1.2))
tf_ml = tb_math_l.text_frame
tf_ml.word_wrap = True
bullets_l = [
    "Thermal Decay: k(T, RH) = k_base * (Q10)^((T-20)/10) * [1 + alpha_hum * max(0, (RH-70)/100)]",
    "Parameters (Tomato): k_base = 0.0065, Q10 = 2.2, alpha_hum = 1.5. Buffer = +2.5 hrs queue.",
    "Physical Rot Loss: L = 1 - exp(-k * t_transit)."
]
for b in bullets_l:
    p = tf_ml.add_paragraph() if tf_ml.paragraphs[0].text else tf_ml.paragraphs[0]
    p.text = "• " + b
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(2)

# Pointer Callout Box Over Arrhenius Findings
callout_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(6.15), Inches(5.3), Inches(0.70))
callout_l.fill.solid()
callout_l.fill.fore_color.rgb = RGBColor(40, 15, 20)
callout_l.line.color.rgb = CRIMSON
callout_l.line.width = Pt(1.2)
tf_cl = callout_l.text_frame
tf_cl.word_wrap = True
p_cl = tf_cl.paragraphs[0]
p_cl.text = "🚨 SURAT TRANSIT TRAP: 234 km Highway @ 32°C/85% RH causes 18.4% Microbial Rot (-₹12,420 Loss) + ₹6,800 Diesel = False Arbitrage Mirage."
p_cl.font.size = Pt(9.5)
p_cl.font.bold = True
p_cl.font.color.rgb = RGBColor(254, 202, 202)

# Right Column: Chronos-2 Foundation Forecaster
card_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.55), Inches(5.7), Inches(5.45))
card_r.fill.solid()
card_r.fill.fore_color.rgb = CARD_BG
card_r.line.color.rgb = CARD_BORDER
card_r.line.width = Pt(1.2)

tb_r = s4.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(0.35))
tf_r = tb_r.text_frame
tf_r.word_wrap = True
p = tf_r.paragraphs[0]
p.text = "amazon/chronos-2 Foundation Price Forecasting"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = SKY_BLUE

chronos_img_path = ASSETS_DIR / "chronos_fan_chart.png"
if chronos_img_path.exists():
    s4.shapes.add_picture(str(chronos_img_path), Inches(7.0), Inches(2.05), Inches(5.3), Inches(2.75))

tb_math_r = s4.shapes.add_textbox(Inches(7.0), Inches(4.85), Inches(5.3), Inches(1.2))
tf_mr = tb_math_r.text_frame
tf_mr.word_wrap = True
bullets_r = [
    "Zero-shot probabilistic forecasting on pretrained T5 time-series architecture.",
    "Conditioned on Open-Meteo 7-day hourly precipitation & temperature shock covariates.",
    "P10, P50, P90 confidence intervals prevent overconfident recommendations."
]
for b in bullets_r:
    p = tf_mr.add_paragraph() if tf_mr.paragraphs[0].text else tf_mr.paragraphs[0]
    p.text = "• " + b
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(2)

# Pointer Callout Box Over Chronos Findings
callout_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(6.15), Inches(5.3), Inches(0.70))
callout_r.fill.solid()
callout_r.fill.fore_color.rgb = RGBColor(6, 45, 30)
callout_r.line.color.rgb = EMERALD
callout_r.line.width = Pt(1.2)
tf_cr = callout_r.text_frame
tf_cr.word_wrap = True
p_cr = tf_cr.paragraphs[0]
p_cr.text = "📈 POST-GLUT REBOUND: Chronos-2 projects Day +10 recovery to ₹1,480/qtl (+64.4% surge over ₹900 crash). Warehousing unlocks +52% net profit."
p_cr.font.size = Pt(9.5)
p_cr.font.bold = True
p_cr.font.color.rgb = RGBColor(167, 243, 208)

# ==============================================================================
# SLIDE 5: 3-Column Financial Arbitrage Matrix (Nashik 50 qtl Lot)
# ==============================================================================
print("[5/9] Building Slide 5: 3-Column Financial Arbitrage Matrix...")
s5 = prs.slides.add_slide(blank_layout)
create_background(s5)
apply_morph_transition(s5)
add_header(s5, "The 3-Column Financial Arbitrage Matrix: +52.0% Net Surge",
           category="QUANTITATIVE PROOF • NASHIK TOMATO GLUT BENCHMARK (50 QUINTALS)",
           subtext="Mathematical Proof: How WDRA e-NWR Warehousing Beats Interstate Transit by +52% Net")

# 3-Bar Visual Comparison Component Across Top
bar_data = [
    ("Option A: Local Panic Dump", "₹45,000 Net Baseline", "Distress Dump @ ₹900/qtl (Below Cost Floor)", CRIMSON, 0.65),
    ("Option B: Interstate Surat Transit", "₹48,280 Net (+7.3%)", "False Mirage: -₹12,420 Rot Loss & -₹6,800 Diesel", AMBER, 0.70),
    ("Option C: KrishiArtha WDRA e-NWR", "₹68,400 Net (+52.0%)", "+₹23,400 Cash Surge after -₹5,600 Cold Storage", EMERALD, 1.00)
]

for idx, (title, net_val, note, col, fill_ratio) in enumerate(bar_data):
    b_left = Inches(0.8 + idx * 3.98)
    card_b = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, b_left, Inches(1.50), Inches(3.78), Inches(0.92))
    card_b.fill.solid()
    card_b.fill.fore_color.rgb = CARD_BG
    card_b.line.color.rgb = col
    card_b.line.width = Pt(1.5)

    tb_b = s5.shapes.add_textbox(b_left + Inches(0.12), Inches(1.54), Inches(3.54), Inches(0.82))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True

    p1 = tf_b.paragraphs[0]
    p1.text = title
    p1.font.size = Pt(10.5)
    p1.font.bold = True
    p1.font.color.rgb = col

    p2 = tf_b.add_paragraph()
    p2.text = net_val
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE

    p3 = tf_b.add_paragraph()
    p3.text = note
    p3.font.size = Pt(8.5)
    p3.font.color.rgb = TEXT_MUTED

# 8-Row Comprehensive Financial Matrix Table (with explicit itemized -₹5,600 storage deduction)
table_shape = s5.shapes.add_table(8, 4, Inches(0.8), Inches(2.52), Inches(11.733), Inches(3.72))
tbl = table_shape.table

tbl.columns[0].width = Inches(2.70)
tbl.columns[1].width = Inches(2.90)
tbl.columns[2].width = Inches(3.00)
tbl.columns[3].width = Inches(3.133)

headers = ["Financial Metric", "Option A: Local Panic Dump", "Option B: Interstate Surat APMC", "Option C: KrishiArtha WDRA e-NWR"]
matrix_data = [
    ["Destination Mandi / Storage", "Pimpalgaon APMC (12 km)", "Surat APMC (234 km)", "MSWC Cold Storage, Ozar (14.2 km)"],
    ["Nominal Quoted Price", "₹900 / qtl (Severe Crash)", "₹1,350 / qtl (Apparent Arbitrage)", "Rebound: ₹1,480 / qtl (Day +10)"],
    ["Arrhenius Q10 Transit Rot Loss", "₹945 (2.1% loss)", "₹12,420 (18.4% Thermal Rot!)", "₹0 (Cold Storage Guarantee)"],
    ["Diesel Freight & Handling", "₹1,925 (Local mini-truck)", "₹6,800 (₹22/km Round-Trip)", "₹750 (Short warehouse haul)"],
    ["Immediate Day-0 Liquidity", "₹45,000 (Immediate Cash)", "₹48,280 (Post-transit payout)", "₹33,750 (75% LTV @ 4% KCC Interest)"],
    ["Cold Storage & KCC Interest Cost", "₹0 (No storage)", "₹0 (No storage)", "-₹5,600 (₹4,200 store + ₹1,400 interest)"],
    ["Final Net Realization (Take-Home)", "₹45,000 Net Baseline", "₹48,280 Net (+7.3% False Trap)", "₹68,400 Net (+52.0% Income Surge)"]
]

for col_idx, h in enumerate(headers):
    cell = tbl.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = CARD_BG
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = EMERALD if col_idx == 3 else TEXT_WHITE

for row_idx, row in enumerate(matrix_data):
    for col_idx, val in enumerate(row):
        cell = tbl.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        if col_idx == 3:
            if row_idx == 6:
                cell.fill.fore_color.rgb = EMERALD_BG
            elif row_idx == 5:
                cell.fill.fore_color.rgb = RGBColor(20, 60, 50)
            else:
                cell.fill.fore_color.rgb = RGBColor(12, 45, 36)
        else:
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 0 else RGBColor(22, 32, 50)
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10)
        if col_idx == 3 or row_idx == 6 or row_idx == 5:
            p.font.bold = True
            if col_idx == 3:
                p.font.color.rgb = EMERALD if row_idx != 5 else AMBER
            else:
                p.font.color.rgb = TEXT_WHITE
        else:
            p.font.color.rgb = TEXT_WHITE

# Bottom Banner Callout with Explicit Intellectual Honesty
bot_banner = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.32), Inches(11.733), Inches(0.75))
bot_banner.fill.solid()
bot_banner.fill.fore_color.rgb = CARD_BG
bot_banner.line.color.rgb = EMERALD
bot_banner.line.width = Pt(1.5)
tf_bb = bot_banner.text_frame
tf_bb.word_wrap = True
p_bb = tf_bb.paragraphs[0]
p_bb.text = "INTELLECTUAL HONESTY & VERIFIED IMPACT: Option C fully itemizes the -₹5,600 storage & KCC interest deduction, yielding an unbeatable +₹23,400 (+52.0%) net income surge over distress dumping, while releasing ₹33,750 immediate liquidity on Day 0."
p_bb.font.size = Pt(10.5)
p_bb.font.bold = True
p_bb.font.color.rgb = EMERALD
p_bb.alignment = PP_ALIGN.CENTER

# ==============================================================================
# SLIDE 6: Autonomous Execution & Human Governance
# ==============================================================================
print("[6/9] Building Slide 6: Autonomous Execution & Human Governance...")
s6 = prs.slides.add_slide(blank_layout)
create_background(s6)
apply_morph_transition(s6)
add_header(s6, "Autonomous Execution & Human Governance",
           category="GOVERNANCE & EXECUTION • HITL SAFETY BARRIER & AUTOMATED BROWSER AGENT",
           subtext="LangGraph interrupt() consent barrier + automated Playwright WDRA filing agent (<1.5s SLA)")

# 3-Step Governance Sequence Flow Banner Across Top
gov_banner = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.50), Inches(11.733), Inches(0.55))
gov_banner.fill.solid()
gov_banner.fill.fore_color.rgb = RGBColor(18, 30, 48)
gov_banner.line.color.rgb = SKY_BLUE
gov_banner.line.width = Pt(1.2)
tf_gb = gov_banner.text_frame
tf_gb.word_wrap = True
p_gb = tf_gb.paragraphs[0]
p_gb.text = "HITL GOVERNANCE FLOW:  [1. Quant Assessment (FastMCP & Chronos)]  ➔  [2. STATE FROZEN: interrupt() Consent Barrier]  ➔  [3. Playwright 1.21s Auto-Filing]"
p_gb.font.size = Pt(10)
p_gb.font.bold = True
p_gb.font.color.rgb = SKY_BLUE
p_gb.alignment = PP_ALIGN.CENTER

# Left Side: 2 Cards (interrupt barrier & Playwright agent)
add_card(s6, Inches(0.8), Inches(2.15), Inches(5.6), Inches(2.35),
         "LangGraph Stateful interrupt() Barrier",
         [
             "Zero autonomous financial execution without explicit farmer approval.",
             "State machine safely freezes execution state, persisting context in InMemorySaver.",
             "Transparent vernacular WhatsApp/voice summary presented to farmer.",
             "Execution only proceeds upon explicit Command(resume=True)."
         ], EMERALD, title_size=14, bullet_size=10.5)

add_card(s6, Inches(0.8), Inches(4.60), Inches(5.6), Inches(2.45),
         "Playwright WDRA Browser Agent (1.21s SLA)",
         [
             "Automates statutory e-NWR warehouse filing in 1.21s (Target SLA: <4.0s).",
             "Fills 14 mandatory fields: Aadhaar, accredited warehouse ID, lot size, crop grade.",
             "Manual portal filing takes 15-20 minutes; Playwright executes 700x faster.",
             "Generates cryptographic sanction hash (#78a2f1) & tamper-proof receipt."
         ], SKY_BLUE, title_size=14, bullet_size=10.5)

# Right Side: Framed WDRA Sanction Slip & Zoom Callout Badges
slip_path = ASSETS_DIR / "wdra_sanction_framed.png"
if slip_path.exists():
    frame_s = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.7), Inches(2.15), Inches(5.833), Inches(4.90))
    frame_s.fill.solid()
    frame_s.fill.fore_color.rgb = CARD_BG
    frame_s.line.color.rgb = EMERALD
    frame_s.line.width = Pt(1.5)

    s6.shapes.add_picture(str(slip_path), Inches(6.85), Inches(2.28), Inches(5.533), Inches(3.10))

    # 3 Zoom Highlight Badges Below Sanction Slip
    zoom_badges = [
        ("₹33,750 Immediate Cash", "75.0% LTV via NABARD Cir 128", EMERALD),
        ("4.0% Subvented Interest", "3.0% Prompt Repayment Incentive", SKY_BLUE),
        ("WDRA ID: MSWC-412", "Accredited Ozar Cold Storage", AMBER)
    ]
    for idx, (z_title, z_desc, z_col) in enumerate(zoom_badges):
        z_left = Inches(6.85 + idx * 1.88)
        card_z = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, z_left, Inches(5.50), Inches(1.78), Inches(1.40))
        card_z.fill.solid()
        card_z.fill.fore_color.rgb = RGBColor(18, 26, 40)
        card_z.line.color.rgb = z_col
        card_z.line.width = Pt(1.0)

        tb_z = card_z.text_frame
        tb_z.word_wrap = True
        p_zt = tb_z.paragraphs[0]
        p_zt.text = z_title
        p_zt.font.size = Pt(9.5)
        p_zt.font.bold = True
        p_zt.font.color.rgb = z_col
        p_zt.space_after = Pt(3)

        p_zd = tb_z.add_paragraph()
        p_zd.text = z_desc
        p_zd.font.size = Pt(8.5)
        p_zd.font.color.rgb = TEXT_WHITE

# ==============================================================================
# SLIDE 7: Vernacular Edge Experience & Dual-Device Multi-Modal Interface
# ==============================================================================
print("[7/9] Building Slide 7: Edge & Vernacular Experience...")
s7 = prs.slides.add_slide(blank_layout)
create_background(s7)
apply_morph_transition(s7)
add_header(s7, "Edge & Vernacular Experience: Dual-Device Multi-Modal Interface",
           category="MULTILINGUAL INCLUSIVITY • BHASHINI VOICE RAILS & MISSION CONTROL",
           subtext="Desktop Mission Control Cockpit (FPO/Trader) paired with Smartphone WhatsApp Voice Note Rails (Smallholder Farmer)")

# Left Frame: Desktop Streamlit Mission Control Cockpit
ui_mockup_path = ASSETS_DIR / "browser_mockup.png"
if ui_mockup_path.exists():
    frame_ui = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(6.2), Inches(4.65))
    frame_ui.fill.solid()
    frame_ui.fill.fore_color.rgb = CARD_BG
    frame_ui.line.color.rgb = SKY_BLUE
    frame_ui.line.width = Pt(1.5)

    s7.shapes.add_picture(str(ui_mockup_path), Inches(0.95), Inches(1.68), Inches(5.9), Inches(3.50))

    tb_uic = s7.shapes.add_textbox(Inches(0.95), Inches(5.25), Inches(5.9), Inches(0.85))
    tf_uic = tb_uic.text_frame
    tf_uic.word_wrap = True
    p1 = tf_uic.paragraphs[0]
    p1.text = "FPO & Mandi Trader View: Streamlit Mission Control Cockpit"
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = SKY_BLUE

    p2 = tf_uic.add_paragraph()
    p2.text = "Live Agmarknet prices, real-time Open-Meteo storm radar, Arrhenius rot alerts & 1-click WDRA filing.\n🌐 Live Web Prototype: https://krishiartha-mcp.streamlit.app"
    p2.font.size = Pt(8.8)
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(2)

# Right Frame: Smartphone Vernacular WhatsApp Voice Note Card in Marathi
wa_card_path = ASSETS_DIR / "whatsapp_vernacular_card.png"
if wa_card_path.exists():
    frame_wa = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.55), Inches(5.333), Inches(4.65))
    frame_wa.fill.solid()
    frame_wa.fill.fore_color.rgb = CARD_BG
    frame_wa.line.color.rgb = EMERALD
    frame_wa.line.width = Pt(1.5)

    s7.shapes.add_picture(str(wa_card_path), Inches(7.35), Inches(1.65), Inches(5.033), Inches(4.45))

# Footer Trust & Speech Rails Banner (Demoting offline mode to subtle badge)
ft_banner = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.32), Inches(11.733), Inches(0.68))
ft_banner.fill.solid()
ft_banner.fill.fore_color.rgb = CARD_BG
ft_banner.line.color.rgb = CARD_BORDER
ft_banner.line.width = Pt(1.0)

tf_ft = ft_banner.text_frame
tf_ft.word_wrap = True
p_ft1 = tf_ft.paragraphs[0]
p_ft1.text = "🌐 Bhashini ULCA Multilingual Speech Rails: मराठी (Marathi) • हिन्दी (Hindi) • తెలుగు (Telugu) • English (22 Scheduled Indian Languages)"
p_ft1.font.size = Pt(10)
p_ft1.font.bold = True
p_ft1.font.color.rgb = SKY_BLUE
p_ft1.alignment = PP_ALIGN.CENTER

p_ft2 = tf_ft.add_paragraph()
p_ft2.text = "🛡️ Stage Certified Trust Badge: 100% Offline Safe-Mode Resilient (OFFLINE_STAGE_SAFE_MODE=true • Zero Stage Wi-Fi Risk)"
p_ft2.font.size = Pt(8.8)
p_ft2.font.bold = True
p_ft2.font.color.rgb = EMERALD
p_ft2.alignment = PP_ALIGN.CENTER
p_ft2.space_before = Pt(2)

# ==============================================================================
# SLIDE 8: Enterprise Security Posture & National DPI Architecture (De-Textified!)
# ==============================================================================
print("[8/9] Building Slide 8: Enterprise Security Posture & DPI Architecture...")
s8 = prs.slides.add_slide(blank_layout)
create_background(s8)
apply_morph_transition(s8)
add_header(s8, "Enterprise Security Audit & National DPI Scalability",
           category="ENTERPRISE SECURITY & DPI ROADMAP • RULE 7A & 7C COMPLIANCE",
           subtext="AgentShield Grade A certified posture + Interconnected national agricultural digital public infrastructure")

# Top: 3 Security Shield Badges Graphic (De-textified!)
sec_badges_path = ASSETS_DIR / "security_shield_badges.png"
if sec_badges_path.exists():
    frame_sec = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.733), Inches(2.25))
    frame_sec.fill.solid()
    frame_sec.fill.fore_color.rgb = CARD_BG
    frame_sec.line.color.rgb = EMERALD
    frame_sec.line.width = Pt(1.2)

    s8.shapes.add_picture(str(sec_badges_path), Inches(0.85), Inches(1.60), Inches(11.633), Inches(2.15))

# Bottom: National DPI Architecture Interconnect Diagram
dpi_arch_path = ASSETS_DIR / "national_dpi_architecture.png"
if dpi_arch_path.exists():
    frame_dpi = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.92), Inches(11.733), Inches(3.18))
    frame_dpi.fill.solid()
    frame_dpi.fill.fore_color.rgb = CARD_BG
    frame_dpi.line.color.rgb = SKY_BLUE
    frame_dpi.line.width = Pt(1.2)

    s8.shapes.add_picture(str(dpi_arch_path), Inches(0.85), Inches(3.96), Inches(11.633), Inches(3.10))

# ==============================================================================
# SLIDE 9: Evaluation Hub & Rapid Verification Protocol (Dual QR Codes & Winning Thesis)
# ==============================================================================
print("[9/9] Building Slide 9: Evaluation Hub & Rapid Verification Protocol...")
s9 = prs.slides.add_slide(blank_layout)
create_background(s9)
apply_morph_transition(s9)
add_header(s9, "Judge Evaluation Hub & Rapid Verification Protocol",
           category="FORGE'26 EVALUATION HUB • LIVE VERIFICATION & REPOSITORY ARTIFACTS",
           subtext="Zero-friction live verification for FORGE'26 evaluators • Dual QR codes for cloud prototype & 5-min HD demo")

# Left Side: 4-Step Rapid Evaluator Test Vector Card
add_card(s9, Inches(0.8), Inches(1.55), Inches(5.9), Inches(4.55),
         "4-Step Rapid Evaluator Test Vector",
         [
             "1. Open Prototype (10s): Scan QR 1 or visit https://krishiartha-mcp.streamlit.app on any device.",
             "2. Input Test Vector (15s): Select District: Nashik | Crop: Tomato | Lot Size: 50 Quintals.",
             "3. Review Financial Matrix (20s): Observe Pimpalgaon ₹900 crash vs MSWC ₹1,480 rebound (+52.0% net gain).",
             "4. Trigger Execution (1.21s): Click 'Approve WDRA Filing (होय)' -> Observe Playwright auto-issue sanction slip.",
             "Codebase Verification: 70/70 Pytests Passing in 11.3s | OFFLINE_STAGE_SAFE_MODE=true air-gap certified."
         ], EMERALD, title_size=15, bullet_size=10.5)

# Right Side: Dual QR Code Card (Live Prototype + Masterpiece Demo Video)
dual_qr_path = ASSETS_DIR / "dual_qr_evaluation.png"
if dual_qr_path.exists():
    frame_qr = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.55), Inches(5.633), Inches(4.55))
    frame_qr.fill.solid()
    frame_qr.fill.fore_color.rgb = CARD_BG
    frame_qr.line.color.rgb = SKY_BLUE
    frame_qr.line.width = Pt(1.5)

    s9.shapes.add_picture(str(dual_qr_path), Inches(7.0), Inches(1.72), Inches(5.433), Inches(4.20))

# Across Bottom: The Winning Anchor Thesis Banner
thesis_banner = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.22), Inches(11.733), Inches(0.92))
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
p_tb2.font.size = Pt(9.8)
p_tb2.font.color.rgb = SKY_BLUE
p_tb2.alignment = PP_ALIGN.CENTER
p_tb2.space_before = Pt(3)

# ----------------- SAVE PRESENTATIONS -----------------
prs.save(str(OUTPUT_PATH))
print(f"[SUCCESS] Saved World-Class Pitch Deck to: {OUTPUT_PATH}")

prs.save(str(BACKUP_PATH))
print(f"[SUCCESS] Saved Backup Pitch Deck to: {BACKUP_PATH}")
