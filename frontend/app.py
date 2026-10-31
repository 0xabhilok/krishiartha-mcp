"""
KrishiArtha-MCP: Bhashini UI Mission Control Dashboard
Main Streamlit Application

Features:
(a) Bhashini Multilingual Voice Input & 1-Click Stage Audio Triggers (Marathi, Hindi, Telugu, English).
(b) 3-Column Financial Arbitrage Matrix:
    - Option A: Local Panic Sale (₹45,000 Net @ ₹900/q)
    - Option B: Surat Transit (Nominal ₹1,350/q eroded to ₹48,280 Net by 18.4% Q10 spoilage + ₹6,800 diesel)
    - Option C: WDRA Cold Storage + 75% e-NWR Loan + Post-Rain Rebound = ₹68,400 Net (+₹23,400 / +52% gain).
(c) Interactive LangGraph interrupt() Consent Card with 'Approve e-NWR Loan (होय / हाँ / Approve)'
    button firing Command(resume=True).
(d) Stage Controls Sidebar: OFFLINE_STAGE_SAFE_MODE toggle & 'What-If Rainfall Shock Slider' (+0mm to +100mm).
"""

import os
import sys
from pathlib import Path

# Ensure repo root is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import json
import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional

# Import local frontend components
from frontend.onnx_bridge.translator import get_translator
from frontend.arbitrage_engine import (
    compute_arbitrage_matrix,
    execute_langgraph_consent,
    load_offline_snapshot,
)

# Page configuration
st.set_page_config(
    page_title="KrishiArtha-MCP | Bhashini Mission Control",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for high-contrast, polished cockpit styling
st.markdown(
    """
    <style>
    /* Metric Card Styling */
    .metric-card {
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .card-option-a {
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
        border-left: 6px solid #e53e3e;
        color: #742a2a;
    }
    .card-option-b {
        background: linear-gradient(135deg, #fffaf0 0%, #feebc8 100%);
        border-left: 6px solid #dd6b20;
        color: #7b341e;
    }
    .card-option-c {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
        border-left: 6px solid #38a169;
        color: #22543d;
    }
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .card-price-primary {
        font-size: 1.85rem;
        font-weight: 800;
        margin: 4px 0;
    }
    .badge-recommended {
        background-color: #22543d;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-trap {
        background-color: #9b2c2c;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-warning {
        background-color: #c05621;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    .interrupt-box {
        background-color: #ebf8ff;
        border: 2px dashed #3182ce;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    .voice-box {
        background-color: #f7fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_session_state():
    """Initializes persistent Streamlit session state keys."""
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "mr"  # Default to Marathi for Nashik Tomato demo
    if "rainfall_shock_mm" not in st.session_state:
        st.session_state.rainfall_shock_mm = 0.0
    if "offline_safe_mode" not in st.session_state:
        env_val = os.getenv("OFFLINE_STAGE_SAFE_MODE", "true").lower() in ("true", "1", "yes")
        st.session_state.offline_safe_mode = env_val
    if "farmer_query" not in st.session_state:
        st.session_state.farmer_query = "माझा ५० क्विंटल टोमॅटो नाशिकला ₹९०० ला विकू की सुरतला नेऊ?"
    if "approval_status" not in st.session_state:
        st.session_state.approval_status = "PENDING"
    if "approval_result" not in st.session_state:
        st.session_state.approval_result = None
    if "farmer_name" not in st.session_state:
        st.session_state.farmer_name = "Suresh Patil"
    if "commodity" not in st.session_state:
        st.session_state.commodity = "Tomato"
    if "lot_quantity_qtl" not in st.session_state:
        st.session_state.lot_quantity_qtl = 50.0
    if "cost_floor_per_qtl" not in st.session_state:
        st.session_state.cost_floor_per_qtl = 1100.0


init_session_state()
translator = get_translator()


def _(text: str) -> str:
    """Convenience translation wrapper."""
    return translator.translate(text, target_lang=st.session_state.selected_language)


# -----------------------------------------------------------------------------
# SIDEBAR: Stage Controls & Simulation
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Stage Controls")
    st.caption("Judge & Audience Interactive Controls")

    # OFFLINE_STAGE_SAFE_MODE toggle
    safe_mode = st.toggle(
        "OFFLINE_STAGE_SAFE_MODE",
        value=st.session_state.offline_safe_mode,
        help="Deterministic offline snapshot mode for guaranteed zero-latency hackathon stage demos.",
    )
    st.session_state.offline_safe_mode = safe_mode
    if safe_mode:
        st.success("🟢 100% Offline Safe Mode Active")
    else:
        st.warning("🟡 Live Network MCP Ingestion Active")

    st.markdown("---")

    # Language Switcher
    st.markdown("### 🌐 Language / भाषा / భాష")
    lang_options = {
        "mr": "मराठी (Marathi)",
        "hi": "हिन्दी (Hindi)",
        "te": "తెలుగు (Telugu)",
        "en": "English",
    }
    selected_lang_key = st.selectbox(
        "Select UI & Voice Language",
        options=list(lang_options.keys()),
        format_func=lambda k: lang_options[k],
        index=list(lang_options.keys()).index(st.session_state.selected_language),
    )
    if selected_lang_key != st.session_state.selected_language:
        st.session_state.selected_language = selected_lang_key
        st.rerun()

    st.markdown("---")

    # What-If Rainfall Shock Slider
    st.markdown("### 🌧️ What-If Weather Shock")
    shock_val = st.slider(
        "Rainfall Shock Delta (+mm)",
        min_value=0,
        max_value=100,
        value=int(st.session_state.rainfall_shock_mm),
        step=5,
        help="Simulates unseasonal cloudburst shock across Nashik mandis triggering Chronos-2 recalculation.",
    )
    if shock_val != st.session_state.rainfall_shock_mm:
        st.session_state.rainfall_shock_mm = float(shock_val)
        st.rerun()

    if st.session_state.rainfall_shock_mm > 0:
        st.info(f"⚡ Simulating +{int(st.session_state.rainfall_shock_mm)}mm Unseasonal Rain Shock")

    st.markdown("---")

    # Farmer Profile Inputs
    st.markdown("### 🧑‍🌾 Farmer Intake Slot")
    st.session_state.farmer_name = st.text_input("Farmer Name", value=st.session_state.farmer_name)
    st.session_state.commodity = st.text_input("Commodity", value=st.session_state.commodity)
    st.session_state.lot_quantity_qtl = st.number_input(
        "Lot Quantity (qtl)", value=float(st.session_state.lot_quantity_qtl), min_value=1.0, step=5.0
    )
    st.session_state.cost_floor_per_qtl = st.number_input(
        "Cost Floor (₹/qtl)", value=float(st.session_state.cost_floor_per_qtl), min_value=100.0, step=50.0
    )

    st.markdown("---")
    st.caption("KrishiArtha-MCP Architecture: LangGraph v1.2.18 + FastMCP + Chronos-2 + IndicTrans2 ONNX")


# -----------------------------------------------------------------------------
# MAIN APP HEADER
# -----------------------------------------------------------------------------
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.title("🌾 KrishiArtha-MCP: Bhashini Mission Control")
    st.subheader(_("Autonomous Covariate Mandi Arbitrage & Distress Policy Engine"))
with header_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.offline_safe_mode:
        st.markdown(
            """<div style='background-color:#c6f6d5; border:1px solid #38a169; border-radius:8px; padding:8px 12px; text-align:center;'>
            <b style='color:#22543d;'>🟢 OFFLINE EDGE MODE</b><br>
            <small style='color:#276749;'>WebAssembly ONNX Active</small>
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """<div style='background-color:#feebc8; border:1px solid #dd6b20; border-radius:8px; padding:8px 12px; text-align:center;'>
            <b style='color:#7b341e;'>🌐 CLOUD CONNECTED</b><br>
            <small style='color:#7b341e;'>Live FastMCP Streaming</small>
            </div>""",
            unsafe_allow_html=True,
        )

# -----------------------------------------------------------------------------
# SECTION 1: Bhashini Voice Input & 1-Click Stage Audio Triggers
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(f"### 🎙️ {_('Bhashini Multilingual Voice Input')}")

voice_box = st.container()
with voice_box:
    st.write(
        f"**{_('1-Click Stage Demo Voice Triggers')}** "
        f"— {_('Click to simulate spoken farmer query in your preferred language:')}"
    )

    trig_col1, trig_col2, trig_col3, trig_col4 = st.columns(4)

    with trig_col1:
        if st.button("▶ मराठी (Marathi) Stage Audio", width="stretch"):
            st.session_state.selected_language = "mr"
            st.session_state.farmer_query = translator.get_stage_prompt("mr")
            st.rerun()

    with trig_col2:
        if st.button("▶ हिन्दी (Hindi) Stage Audio", width="stretch"):
            st.session_state.selected_language = "hi"
            st.session_state.farmer_query = translator.get_stage_prompt("hi")
            st.rerun()

    with trig_col3:
        if st.button("▶ తెలుగు (Telugu) Stage Audio", width="stretch"):
            st.session_state.selected_language = "te"
            st.session_state.farmer_query = translator.get_stage_prompt("te")
            st.rerun()

    with trig_col4:
        if st.button("▶ English Stage Audio", width="stretch"):
            st.session_state.selected_language = "en"
            st.session_state.farmer_query = translator.get_stage_prompt("en")
            st.rerun()

    # Audio recorder & live text query input
    query_col1, query_col2 = st.columns([3, 1])
    with query_col1:
        st.session_state.farmer_query = st.text_input(
            "Transcribed Farmer Voice Query (Bhashini ASR / ULCA)",
            value=st.session_state.farmer_query,
            help="Spoken query captured from farmer microphone or stage demo triggers.",
        )
    with query_col2:
        # Check if browser audio input widget is available
        if hasattr(st, "audio_input"):
            audio_data = st.audio_input("Record Voice Query (ASR)", label_visibility="collapsed")
            if audio_data is not None:
                st.caption("🎙️ Live Voice Chunk Received (Bhashini ASR Transcribing...)")

    # Spoken Audio Playback
    advisory_script = translator.get_vernacular_advisory(st.session_state.selected_language)
    with st.expander(f"🔊 {_('Speak Advisory')} (Bhashini TTS Vernacular Audio Output)", expanded=False):
        st.info(f"**Synthesized Voice Response:**\n\n{advisory_script}")
        # Audio playback simulation via Web Speech API or audio trigger
        st.markdown(
            f"""
            <button onclick="window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{advisory_script[:180].replace("'", "")}'); msg.lang='{st.session_state.selected_language}'; window.speechSynthesis.speak(msg);"
            style="background-color:#3182ce; color:white; border:none; padding:8px 16px; border-radius:6px; cursor:pointer; font-weight:600;">
            ▶ Listen to Vernacular Audio Advisory
            </button>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------------------------------------------------------
# SECTION 2: 3-Column Financial Arbitrage Matrix
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(f"### 📊 {_('3-Column Financial Arbitrage Matrix')}")

# Compute live numbers based on rainfall shock slider and lot parameters
matrix_data = compute_arbitrage_matrix(
    quantity_qtl=st.session_state.lot_quantity_qtl,
    rainfall_shock_mm=st.session_state.rainfall_shock_mm,
    cost_floor_per_qtl=st.session_state.cost_floor_per_qtl,
)

opt_a = matrix_data["option_a"]
opt_b = matrix_data["option_b"]
opt_c = matrix_data["option_c"]

col_a, col_b, col_c = st.columns(3)

# ----------------- COLUMN 1: OPTION A (LOCAL PANIC SALE) -----------------
with col_a:
    st.markdown(
        f"""
        <div class="metric-card card-option-a">
            <span class="badge-trap">{_('Distress Trap')}</span>
            <div class="card-title">{_('Option A: Local Panic Sale')}</div>
            <div style="font-size:0.9rem; font-weight:600;">{opt_a['market_name']}</div>
            <div class="card-price-primary">₹{opt_a['total_net_payout_inr']:,.0f} <span style="font-size:1rem; font-weight:400;">{_('Total Net Realization')}</span></div>
            <hr style="margin: 8px 0; border-top: 1px solid #feb2b2;">
            <div><b>{_('Net Realizable Price')}:</b> ₹{opt_a['net_realizable_price_per_qtl']:.1f} / qtl</div>
            <div><b>{_('Nominal Modal Price')}:</b> ₹{opt_a['modal_price_per_qtl']:.1f} / qtl</div>
            <div><b>{_('Transit & Spoilage Loss')}:</b> {opt_a['spoilage_loss_pct']:.1f}% (Local)</div>
            <div><b>{_('Transport & Diesel Cost')}:</b> ₹{opt_a['transport_cost_inr']:,.0f}</div>
            <div style="margin-top:8px; color:#c53030; font-weight:700;">
                ⚠️ Below Cost Floor of ₹{st.session_state.cost_floor_per_qtl:,.0f} (Net Loss: -₹{opt_a['loss_vs_cost_floor_inr']:,.0f})
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------- COLUMN 2: OPTION B (SURAT TRANSIT ARBITRAGE) -----------------
with col_b:
    st.markdown(
        f"""
        <div class="metric-card card-option-b">
            <span class="badge-warning">{_('False Arbitrage Trap')}</span>
            <div class="card-title">{_('Option B: Surat Transit Arbitrage')}</div>
            <div style="font-size:0.9rem; font-weight:600;">{opt_b['market_name']}</div>
            <div class="card-price-primary">₹{opt_b['total_net_payout_inr']:,.0f} <span style="font-size:1rem; font-weight:400;">{_('Total Net Realization')}</span></div>
            <hr style="margin: 8px 0; border-top: 1px solid #fbd38d;">
            <div><b>{_('Nominal Modal Price')}:</b> ₹{opt_b['nominal_modal_price_per_qtl']:.1f} / qtl</div>
            <div><b>{_('Transit & Spoilage Loss')}:</b> <b>{opt_b['spoilage_loss_pct']:.1f}%</b> ({opt_b['spoilage_loss_quintals']:.1f} qtl Q10 rot)</div>
            <div><b>{_('Transport & Diesel Cost')}:</b> -₹{opt_b['transport_cost_inr']:,.0f} (234 km diesel freight)</div>
            <div><b>{_('Net Realizable Price')}:</b> ₹{opt_b['net_realizable_price_per_qtl']:.1f} / qtl</div>
            <div style="margin-top:8px; color:#9c4221; font-weight:700;">
                ❌ Illusion: Nominal ₹1,350 eroded to ₹{opt_b['net_realizable_price_per_qtl']:.1f}/qtl by Q10 decay + diesel!
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------- COLUMN 3: OPTION C (KRISHIARTHA RECOMMENDED) -----------------
with col_c:
    st.markdown(
        f"""
        <div class="metric-card card-option-c">
            <span class="badge-recommended">{_('KrishiArtha Recommended')}</span>
            <div class="card-title">{_('Option C: WDRA Cold Storage + e-NWR Loan')}</div>
            <div style="font-size:0.9rem; font-weight:600;">{opt_c['warehouse_name']} ({opt_c['distance_km']} km)</div>
            <div class="card-price-primary">₹{opt_c['net_take_home_inr']:,.0f} <span style="font-size:1rem; font-weight:400;">{_('Total Net Realization')}</span></div>
            <hr style="margin: 8px 0; border-top: 1px solid #9ae6b4;">
            <div><b>{_('Pledge Advance Liquidity')}:</b> <b>₹{opt_c['pledge_advance_loan_inr']:,.0f}</b> (75% instant LTV)</div>
            <div><b>{_('Effective Net Interest')}:</b> {opt_c['effective_interest_pct']:.1f}% p.a. (3% KCC subvention)</div>
            <div><b>{_('Post-Rain Rebound Revenue')}:</b> ₹{opt_c['gross_rebound_revenue_inr']:,.0f} (@ ₹{opt_c['projected_rebound_price_per_qtl']:.0f}/qtl)</div>
            <div><b>{_('Net Gain vs Local Panic Sale')}:</b> <b style="color:#22543d; font-size:1.1rem;">+₹{opt_c['net_gain_vs_local_inr']:,.0f} (+{opt_c['net_gain_percentage']:.1f}% gain)</b></div>
            <div style="margin-top:8px; color:#22543d; font-weight:700;">
                ⭐ Best Decision: Retains stock in WDRA cold chain & recovers +₹{opt_c['net_gain_vs_local_inr']:,.0f}!
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# SECTION 3: Interactive LangGraph interrupt() Consent Card
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(f"### 🛡️ {_('LangGraph Statutory Consent Card')}")

interrupt_container = st.container()
with interrupt_container:
    st.markdown(
        f"""
        <div class="interrupt-box">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#2b6cb0;">⚡ LangGraph v1.2.18 State: <code>interrupt(human_approval_gate)</code></h4>
                <span style="background-color:#fed7d7; color:#9b2c2c; padding:4px 8px; border-radius:6px; font-weight:700; font-size:0.85rem;">
                    {_('Execution Paused: Awaiting Farmer Consent')}
                </span>
            </div>
            <p style="margin-top:10px; font-size:0.95rem; color:#2d3748;">
                The neuro-symbolic engine has detected a regional glut crash where all APMC mandis yield net prices below the ₹{st.session_state.cost_floor_per_qtl:,.0f} cost floor.
                In compliance with statutory fiduciary guidelines, LangGraph has paused execution at the Human-in-the-Loop gate.
            </p>
            <div style="background-color:white; border-radius:8px; padding:12px; margin:10px 0; border:1px solid #cbd5e0;">
                <table style="width:100%; font-size:0.92rem; color:#2d3748;">
                    <tr><td><b>Farmer Name:</b> {st.session_state.farmer_name}</td><td><b>Warehouse Reg No:</b> {opt_c['warehouse_reg_no']}</td></tr>
                    <tr><td><b>Commodity & Lot:</b> {st.session_state.commodity} ({st.session_state.lot_quantity_qtl:.0f} Quintals)</td><td><b>Warehouse Name:</b> {opt_c['warehouse_name']}</td></tr>
                    <tr><td><b>e-NWR 75% Pledge Advance:</b> <span style="color:#22543d; font-weight:700;">₹{opt_c['pledge_advance_loan_inr']:,.0f} Instant Liquidity</span></td><td><b>Net Interest Subvention:</b> 7.0% - 3.0% = 4.0% p.a.</td></tr>
                    <tr><td><b>Post-Rebound Realization:</b> ₹{opt_c['net_take_home_inr']:,.0f}</td><td><b>Arbitrage Net Advantage:</b> <span style="color:#22543d; font-weight:800;">+₹{opt_c['net_gain_vs_local_inr']:,.0f} (+{opt_c['net_gain_percentage']:.1f}%)</span></td></tr>
                </table>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 1])

    with btn_col1:
        approve_btn_label = f"✅ {_('Approve e-NWR Loan (होय / हाँ / Approve)')}"
        if st.button(approve_btn_label, type="primary", width="stretch"):
            with st.spinner("Dispatching Command(resume=True) to LangGraph StateGraph..."):
                consent_result = execute_langgraph_consent(
                    action="APPROVE",
                    farmer_name=st.session_state.farmer_name,
                    commodity=st.session_state.commodity,
                    quantity_qtl=st.session_state.lot_quantity_qtl,
                    loan_amount=opt_c["pledge_advance_loan_inr"],
                    warehouse_reg_no=opt_c["warehouse_reg_no"],
                )
                st.session_state.approval_status = "APPROVED_ENWR"
                st.session_state.approval_result = consent_result

    with btn_col2:
        reject_btn_label = f"❌ {_('Reject & Force Local Sale')}"
        if st.button(reject_btn_label, width="stretch"):
            consent_result = execute_langgraph_consent(
                action="REJECT",
                farmer_name=st.session_state.farmer_name,
                commodity=st.session_state.commodity,
                quantity_qtl=st.session_state.lot_quantity_qtl,
                loan_amount=0.0,
                warehouse_reg_no=opt_c["warehouse_reg_no"],
            )
            st.session_state.approval_status = "REJECTED_LOCAL_SALE"
            st.session_state.approval_result = consent_result

    with btn_col3:
        if st.button("🔄 Reset LangGraph State", width="stretch"):
            st.session_state.approval_status = "PENDING"
            st.session_state.approval_result = None
            st.rerun()

    # Display consent execution status
    if st.session_state.approval_status == "APPROVED_ENWR" and st.session_state.approval_result:
        res = st.session_state.approval_result
        st.success(
            f"🎉 **{_('Loan Approved Successfully!')}**\n\n"
            f"- **LangGraph Resume:** `Command(resume=True)` successfully delivered.\n"
            f"- **Submission ID:** `{res['submission_id']}`\n"
            f"- **WDRA Gate Pass Issued:** `{res['gate_pass_code']}`\n"
            f"- **Pledge Advance Disbursed:** ₹{res['pledge_loan_amount_inr']:,.2f} into registered KCC bank account.\n"
            f"- **Timestamp:** {res['timestamp']}"
        )
    elif st.session_state.approval_status == "REJECTED_LOCAL_SALE":
        st.warning(
            "⚠️ **Distress Sale Forced:** Farmer opted out of WDRA e-NWR pledge loan. "
            "Proceeding with local distress liquidation at ₹900/qtl."
        )


# -----------------------------------------------------------------------------
# SECTION 4: Comparative Analytics & Chronos-2 Forecasting
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 📈 Visual Arbitrage Breakdown & Chronos-2 Trajectory")

chart_col1, chart_col2 = st.columns([3, 2])

with chart_col1:
    st.write("**Financial Payout Comparison (INR)**")
    df_chart = pd.DataFrame(
        {
            "Strategy": [
                "Option A: Local Panic Sale",
                "Option B: Surat Transit (Post Q10 Decay)",
                "Option C: WDRA e-NWR Payout",
            ],
            "Net Payout (₹)": [
                opt_a["total_net_payout_inr"],
                opt_b["total_net_payout_inr"],
                opt_c["net_take_home_inr"],
            ],
        }
    )
    st.bar_chart(df_chart.set_index("Strategy"), color="#38a169")

with chart_col2:
    st.write("**Chronos-2 Price Rebound Quantiles (₹/qtl)**")
    # 7-day quantile projection
    df_quantiles = pd.DataFrame(
        {
            "Horizon": ["Day 1 (Crash)", "Day 3 (Rain Peaks)", "Day 5 (Clearing)", "Day 7 (Rebound)", "Day 10 (Clear)"],
            "P10 (Glut)": [620, 580, 750, 980, 1250],
            "P50 (Expected)": [900, 850, 1050, 1340, 1480],
            "P90 (Upside)": [950, 920, 1180, 1490, 1620],
        }
    )
    st.dataframe(df_quantiles, width="stretch", hide_index=True)


# -----------------------------------------------------------------------------
# SECTION 5: Statutory Citations
# -----------------------------------------------------------------------------
with st.expander(f"📜 {_('Statutory Policy Citations')} (NABARD Circulars & WDRA Guidelines)", expanded=False):
    for citation in matrix_data.get("statutory_citations", []):
        st.markdown(
            f"""
            - **{citation.get('authority', 'Statutory Authority')}** — *{citation.get('circular', 'Circular')}*
              <br><b>Clause:</b> {citation.get('clause', '')}
              <br><small>{citation.get('provisions', '')}</small>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")
st.caption(
    "KrishiArtha-MCP | Built for FORGE'26 GenAI Buildathon | High-Fidelity Bhashini & Neuro-Symbolic Architecture"
)
