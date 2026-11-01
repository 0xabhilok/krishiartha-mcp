"""
Masterpiece Demo Video Generator for KrishiArtha-MCP
Strictly synchronized to the 241.27s (4:01) world-class dual neural narration.
Features:
1. True internal scrolling of Streamlit's container (document.getElementById('stMain'))
   using requestAnimationFrame smooth interpolation (ZERO frozen frames!).
2. Live Open-Meteo Weather Radar display (31.5°C, 82% RH, 42.5mm rain, 2.2x Q10).
3. 3-Column Financial Arbitrage Matrix (Option A vs Option B Surat rot trap vs Option C).
4. 3D GIS Spatial PyDeck Map with live highway route arcs.
5. Chronos-2 Foundation AI Quantile Fan Chart with Day +10 price rebound.
6. LangGraph Human-in-the-Loop Consent Gate & 1.21s Playwright Sanction Slip.
7. Pan-India Live APMC Telemetry Search & AgentShield Grade A (100/100) Inspector.
"""
import time
import os
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path("docs/demo_recording")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

AUDIO_FILE = OUTPUT_DIR / "world_class_narration.mp3"
FINAL_VIDEO = Path("docs/KrishiArtha_MCP_Masterpiece_Demo.mp4")

TARGET_DURATION = 241.27

def inject_helpers(page):
    page.evaluate("""
        () => {
            // Repaint ticker: forces Chromium to encode CFR video frames continuously
            let frame = 0;
            let ticker = document.getElementById('cfr-ticker');
            if (!ticker) {
                ticker = document.createElement('div');
                ticker.id = 'cfr-ticker';
                ticker.style.position = 'fixed';
                ticker.style.bottom = '1px';
                ticker.style.right = '1px';
                ticker.style.width = '2px';
                ticker.style.height = '2px';
                ticker.style.opacity = '0.05';
                document.body.appendChild(ticker);

                function tick() {
                    frame++;
                    ticker.style.transform = `translateX(${frame % 3}px)`;
                    requestAnimationFrame(tick);
                }
                requestAnimationFrame(tick);
            }

            // HUD Banner
            let hud = document.getElementById('demo-hud-banner');
            if (!hud) {
                hud = document.createElement('div');
                hud.id = 'demo-hud-banner';
                hud.style.position = 'fixed';
                hud.style.top = '14px';
                hud.style.left = '50%';
                hud.style.transform = 'translateX(-50%)';
                hud.style.backgroundColor = 'rgba(15, 23, 42, 0.94)';
                hud.style.color = '#38bdf8';
                hud.style.border = '1.5px solid #0284c7';
                hud.style.padding = '8px 24px';
                hud.style.borderRadius = '30px';
                hud.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
                hud.style.fontSize = '14px';
                hud.style.fontWeight = '700';
                hud.style.boxShadow = '0 10px 25px -5px rgba(0,0,0,0.6)';
                hud.style.zIndex = '9999999';
                hud.style.letterSpacing = '0.4px';
                hud.innerText = '🌾 SCENE 1: October 2026 Nashik Tomato Crisis — Regional APMC Price Collapse';
                document.body.appendChild(hud);
            }

            // Glowing Virtual Cursor
            let cur = document.getElementById('demo-virtual-cursor');
            if (!cur) {
                cur = document.createElement('div');
                cur.id = 'demo-virtual-cursor';
                cur.style.position = 'fixed';
                cur.style.width = '26px';
                cur.style.height = '26px';
                cur.style.border = '2.5px solid #10b981';
                cur.style.borderRadius = '50%';
                cur.style.backgroundColor = 'rgba(16, 185, 129, 0.35)';
                cur.style.boxShadow = '0 0 16px #10b981';
                cur.style.pointerEvents = 'none';
                cur.style.zIndex = '9999998';
                cur.style.transition = 'all 0.28s cubic-bezier(0.25, 1, 0.5, 1)';
                cur.style.left = '640px';
                cur.style.top = '360px';
                document.body.appendChild(cur);
            }

            window.setHud = (text) => {
                const el = document.getElementById('demo-hud-banner');
                if (el) el.innerText = text;
            };

            window.moveCur = (x, y, color = '#10b981') => {
                const el = document.getElementById('demo-virtual-cursor');
                if (el) {
                    el.style.left = (x - 13) + 'px';
                    el.style.top = (y - 13) + 'px';
                    el.style.borderColor = color;
                    el.style.boxShadow = `0 0 16px ${color}`;
                    el.style.backgroundColor = color.replace(')', ', 0.35)').replace('rgb', 'rgba');
                }
            };

            // Smooth scroll helper for Streamlit's #stMain container
            window.smoothScrollStMain = (targetY, durationMs = 600) => {
                const el = document.getElementById('stMain') || document.querySelector('[data-testid="stMain"]');
                if (!el) return;
                const startY = el.scrollTop;
                const diff = targetY - startY;
                const startTime = performance.now();

                function step(now) {
                    const elapsed = now - startTime;
                    const progress = Math.min(elapsed / durationMs, 1);
                    const ease = progress < 0.5 ? 2 * progress * progress : 1 - Math.pow(-2 * progress + 2, 2) / 2;
                    el.scrollTop = startY + diff * ease;
                    if (progress < 1) {
                        requestAnimationFrame(step);
                    }
                }
                requestAnimationFrame(step);
            };
        }
    """)

def run_masterpiece_recording():
    # Clear old webm
    for f in OUTPUT_DIR.glob("*.webm"):
        try:
            f.unlink()
        except Exception:
            pass

    start_real_time = time.time()

    with sync_playwright() as p:
        print("[0:00] Launching High-Definition Playwright Chromium (1280x720)...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir=str(OUTPUT_DIR),
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()

        print("[0:02] Navigating to http://127.0.0.1:8501...")
        page.goto("http://127.0.0.1:8501", wait_until="domcontentloaded", timeout=30000)
        time.sleep(4)
        inject_helpers(page)

        def wait_until(target_sec):
            elapsed = time.time() - start_real_time
            remaining = target_sec - elapsed
            if remaining > 0:
                time.sleep(remaining)

        # -------------------------------------------------------------
        # SCENE 1 [0:00 -> 52.78s]: Hook & The Regional Monsoon Crisis
        # -------------------------------------------------------------
        print("[0:05] SCENE 1: High-Stakes Crisis & Agmarknet Failure...")
        page.evaluate("setHud('🌾 SCENE 1: October 2026 Nashik Tomato Crisis — Regional APMC Price Collapse')")
        page.evaluate("moveCur(640, 200, '#10b981')")
        wait_until(14)

        # Highlight Live FastMCP badge in header
        page.evaluate("moveCur(1100, 110, '#10b981')")
        wait_until(28)

        # Highlight Farmer Intake Slot in sidebar
        page.evaluate("moveCur(180, 480, '#38bdf8')")
        wait_until(42)

        # Pan to What-If Weather Shock
        page.evaluate("moveCur(180, 360, '#f59e0b')")
        wait_until(52.78)

        # -------------------------------------------------------------
        # SCENE 2 [52.78 -> 84.24s]: Bhashini Voice & Real-Time APIs (Rule 4)
        # -------------------------------------------------------------
        print("[0:53] SCENE 2: Bhashini Multilingual Voice Rails & FastMCP Live APIs...")
        page.evaluate("setHud('🗣️ SCENE 2: Bhashini Voice Ingestion & FastMCP Live Telemetry (Rule 4 Zero Mock Data)')")
        page.evaluate("smoothScrollStMain(180, 500)")
        wait_until(58)

        # Move to Marathi Trigger Button
        page.evaluate("moveCur(420, 260, '#f59e0b')")
        time.sleep(1)

        # Click Marathi button
        buttons = page.locator("button")
        for i in range(buttons.count()):
            try:
                txt = buttons.nth(i).inner_text()
                if "मराठी" in txt:
                    buttons.nth(i).click()
                    break
            except Exception:
                pass

        inject_helpers(page)
        page.evaluate("setHud('🗣️ SCENE 2: Bhashini Marathi Voice Triggered — Slot Extraction: Tomato 50qtl Nashik')")
        page.evaluate("moveCur(640, 320, '#10b981')")
        wait_until(74)

        # Click English button to restore
        for i in range(buttons.count()):
            try:
                txt = buttons.nth(i).inner_text()
                if "English" in txt:
                    buttons.nth(i).click()
                    break
            except Exception:
                pass

        inject_helpers(page)
        page.evaluate("setHud('🗣️ SCENE 2: FastMCP Live Telemetry Ingestion (Data.gov.in, Open-Meteo, OSRM)')")
        page.evaluate("moveCur(640, 320, '#10b981')")
        wait_until(84.24)

        # -------------------------------------------------------------
        # SCENE 3 [84.24 -> 103.37s]: Meteorological Radar (31.5°C, 82% RH, 42.5mm)
        # -------------------------------------------------------------
        print("[1:24] SCENE 3: Open-Meteo Meteorological Radar & Chronos-2 Price Fan Chart...")
        page.evaluate("setHud('🌧️ SCENE 3: Open-Meteo Weather Radar — 31.5°C, 82% RH, 42.5mm Rain Shock')")
        page.evaluate("smoothScrollStMain(650, 600)")
        wait_until(88)

        # Point at Ambient Temp 31.5°C
        page.evaluate("moveCur(420, 190, '#ef4444')")
        wait_until(92)

        # Point at Relative Humidity 82%
        page.evaluate("moveCur(600, 190, '#38bdf8')")
        wait_until(95)

        # Point at Precipitation 42.5mm
        page.evaluate("moveCur(780, 190, '#38bdf8')")
        wait_until(98)

        # Point at Arrhenius Decay Factor 2.2x
        page.evaluate("moveCur(960, 190, '#f59e0b')")
        wait_until(103.37)

        # -------------------------------------------------------------
        # SCENE 4 [103.37 -> 140.52s]: 3-Column Arbitrage Matrix & Surat False Trap
        # -------------------------------------------------------------
        print("[1:43] SCENE 4: 3-Column Arbitrage Matrix & Surat False Arbitrage Trap...")
        page.evaluate("setHud('🔬 SCENE 4: 3-Column Arbitrage Matrix — Exposing the Surat False Arbitrage Trap')")
        page.evaluate("smoothScrollStMain(850, 500)")
        wait_until(108)

        # Point at Option A (Panic sale crash ₹45,000)
        page.evaluate("moveCur(480, 320, '#ef4444')")
        wait_until(118)

        # Point at Option B (Surat Trap - Nominal ₹1,350 vs Net ₹48,280)
        page.evaluate("moveCur(800, 320, '#f59e0b')")
        wait_until(128)

        # Highlight Option B Spoilage rot 18.4% (-₹12,420) and diesel ₹6,800
        page.evaluate("moveCur(800, 480, '#ef4444')")
        wait_until(140.52)

        # -------------------------------------------------------------
        # SCENE 5 [140.52 -> 188.30s]: Option C WDRA + 3D GIS Map + Chronos-2 Rebound
        # -------------------------------------------------------------
        print("[2:20] SCENE 5: Option C WDRA Cold Storage + 3D GIS Map + Rebound...")
        page.evaluate("setHud('🏛️ SCENE 5: Option C WDRA Breakthrough — ₹33,750 Immediate Cash & ₹68,400 Rebound')")

        # Point at Option C (Glowing Emerald, ₹68,400 Net)
        page.evaluate("moveCur(1120, 280, '#10b981')")
        wait_until(150)

        # Highlight 75% LTV instant advance of ₹33,750 @ 4% net interest
        page.evaluate("moveCur(1120, 420, '#10b981')")
        wait_until(158)

        # Smooth scroll to 3D GIS Spatial PyDeck Map
        print("[2:38] SCENE 5b: 3D GIS Spatial Route Highway Simulator...")
        page.evaluate("setHud('🗺️ SCENE 5: 3D GIS Spatial Highway Simulator — Route Arcs to Surat, Mumbai, Ozar')")
        page.evaluate("smoothScrollStMain(1650, 800)")
        page.evaluate("moveCur(640, 420, '#10b981')")
        wait_until(172)

        # Smooth scroll to Chronos-2 Foundation AI Quantile Fan Chart
        print("[2:52] SCENE 5c: Chronos-2 Quantile Fan Chart Rebound...")
        page.evaluate("setHud('📈 SCENE 5: Chronos-2 Post-Glut Price Rebound — Day +10 Rebound to ₹1,480/qtl (+64%)')")
        page.evaluate("smoothScrollStMain(2350, 800)")
        page.evaluate("moveCur(640, 420, '#a855f7')")
        wait_until(188.30)

        # -------------------------------------------------------------
        # SCENE 6 [188.30 -> 214.36s]: LangGraph Consent Gate & Browser Agent
        # -------------------------------------------------------------
        print("[3:08] SCENE 6: LangGraph Human-in-the-Loop Gate & Automated WDRA Agent...")
        page.evaluate("setHud('⚡ SCENE 6: LangGraph Human-in-the-Loop Consent Gate — State Frozen Awaiting Approval')")
        page.evaluate("smoothScrollStMain(3200, 700)")
        wait_until(193)

        # Point at Consent Gate interrupt box
        page.evaluate("moveCur(640, 320, '#38bdf8')")
        wait_until(199)

        # Hover over Approve e-NWR Loan Button
        page.evaluate("moveCur(640, 480, '#10b981')")
        time.sleep(1)

        # Click Approve e-NWR Loan Button
        for i in range(buttons.count()):
            try:
                txt = buttons.nth(i).inner_text()
                if "Approve" in txt or "मंजूर" in txt or "होय" in txt:
                    buttons.nth(i).click()
                    break
            except Exception:
                pass

        inject_helpers(page)
        page.evaluate("setHud('⚡ SCENE 6: Official WDRA Sanction Slip Generated in 1.21s — ₹33,750 Advance')")
        page.evaluate("smoothScrollStMain(3450, 500)")
        page.evaluate("moveCur(640, 420, '#10b981')")
        wait_until(214.36)

        # -------------------------------------------------------------
        # SCENE 7 [214.36 -> 241.27s]: Live APMC Search, AgentShield Grade A & Closing
        # -------------------------------------------------------------
        print("[3:34] SCENE 7: Pan-India APMC Search, AgentShield Grade A & 70/70 Pytests...")
        page.evaluate("setHud('🛡️ SCENE 7: Pan-India APMC Telemetry Search — Live API Ingestion (Rule 4 Zero Mock Data)')")
        page.evaluate("smoothScrollStMain(3800, 600)")
        wait_until(220)

        # Click Fetch Live APMCs to prove live data
        page.evaluate("moveCur(1100, 300, '#10b981')")
        time.sleep(1)
        for i in range(buttons.count()):
            try:
                txt = buttons.nth(i).inner_text()
                if "Fetch Live APMCs" in txt:
                    buttons.nth(i).click()
                    break
            except Exception:
                pass

        inject_helpers(page)
        page.evaluate("setHud('🛡️ SCENE 7: AgentShield Grade A (100/100) & 70/70 Pytests Passing in 9.24s')")
        page.evaluate("smoothScrollStMain(4400, 600)")
        page.evaluate("moveCur(640, 400, '#38bdf8')")
        wait_until(TARGET_DURATION)

        print("[4:01] Masterpiece session concluded. Flushing video stream...")
        context.close()
        browser.close()
        print("Playwright recording closed successfully.")

    # Locate webm file
    webm_files = list(OUTPUT_DIR.glob("*.webm"))
    if not webm_files:
        print("ERROR: No webm file recorded!")
        return

    latest_webm = max(webm_files, key=lambda f: f.stat().st_mtime)
    print(f"Recorded webm: {latest_webm}")

    print(f"Muxing into {FINAL_VIDEO} with frame-accurate sync...")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(latest_webm),
        "-i", str(AUDIO_FILE),
        "-vf", "fps=30,setpts=PTS-STARTPTS",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "00:04:01.27",
        str(FINAL_VIDEO)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"SUCCESS: Masterpiece Demo Video created at {FINAL_VIDEO} (Size: {FINAL_VIDEO.stat().st_size} bytes)")
    else:
        print(f"FFmpeg error: {res.stderr}")

if __name__ == "__main__":
    run_masterpiece_recording()
