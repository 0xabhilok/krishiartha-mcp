"""
Masterpiece Demo Video Generator for KrishiArtha-MCP
Strictly synchronized to the 241.27s (4:01) world-class dual neural narration.
Features continuous frame painting (requestAnimationFrame), dynamic HUD banners,
animated glowing cursor highlights, and automated interactive live workflows.
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

# Timeline offsets matching the 7 dialogue segments (in seconds)
# Seg 1: 0.00 -> 52.78
# Seg 2: 52.78 -> 84.24
# Seg 3: 84.24 -> 103.37
# Seg 4: 103.37 -> 140.52
# Seg 5: 140.52 -> 188.30
# Seg 6: 188.30 -> 214.36
# Seg 7: 214.36 -> 241.27
TARGET_DURATION = 241.27

def inject_helpers(page):
    page.evaluate("""
        () => {
            // Repaint ticker: forces Chromium to encode CFR video frames without dropping
            let frame = 0;
            const ticker = document.createElement('div');
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

            // HUD Banner
            const hud = document.createElement('div');
            hud.id = 'demo-hud-banner';
            hud.style.position = 'fixed';
            hud.style.top = '14px';
            hud.style.left = '50%';
            hud.style.transform = 'translateX(-50%)';
            hud.style.backgroundColor = 'rgba(15, 23, 42, 0.94)';
            hud.style.color = '#38bdf8';
            hud.style.border = '1px solid #0284c7';
            hud.style.padding = '8px 24px';
            hud.style.borderRadius = '30px';
            hud.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
            hud.style.fontSize = '13.5px';
            hud.style.fontWeight = '700';
            hud.style.boxShadow = '0 10px 25px -5px rgba(0,0,0,0.6)';
            hud.style.zIndex = '9999999';
            hud.style.letterSpacing = '0.4px';
            hud.innerText = '🌾 SCENE 1: The October 2026 Monsoon Glut in Nashik';
            document.body.appendChild(hud);

            // Glowing Virtual Cursor
            const cur = document.createElement('div');
            cur.id = 'demo-virtual-cursor';
            cur.style.position = 'fixed';
            cur.style.width = '24px';
            cur.style.height = '24px';
            cur.style.border = '2.5px solid #10b981';
            cur.style.borderRadius = '50%';
            cur.style.backgroundColor = 'rgba(16, 185, 129, 0.35)';
            cur.style.boxShadow = '0 0 14px #10b981';
            cur.style.pointerEvents = 'none';
            cur.style.zIndex = '9999998';
            cur.style.transition = 'all 0.25s cubic-bezier(0.25, 1, 0.5, 1)';
            cur.style.left = '640px';
            cur.style.top = '360px';
            document.body.appendChild(cur);

            window.setHud = (text) => {
                const el = document.getElementById('demo-hud-banner');
                if (el) el.innerText = text;
            };

            window.moveCur = (x, y, color = '#10b981') => {
                const el = document.getElementById('demo-virtual-cursor');
                if (el) {
                    el.style.left = (x - 12) + 'px';
                    el.style.top = (y - 12) + 'px';
                    el.style.borderColor = color;
                    el.style.boxShadow = `0 0 14px ${color}`;
                    el.style.backgroundColor = color.replace(')', ', 0.35)').replace('rgb', 'rgba');
                }
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
        print("[0:00] Launching High-Definition Playwright Chromium...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir=str(OUTPUT_DIR),
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()

        print("[0:02] Navigating to http://127.0.0.1:8501...")
        page.goto("http://127.0.0.1:8501", wait_until="domcontentloaded", timeout=25000)
        time.sleep(3)
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
        page.evaluate("moveCur(400, 120, '#10b981')")
        wait_until(15)

        # Highlight Live FastMCP badge
        page.evaluate("moveCur(1100, 110, '#10b981')")
        wait_until(28)

        # Highlight Farmer Intake Slot
        page.evaluate("moveCur(180, 480, '#38bdf8')")
        wait_until(42)

        page.evaluate("moveCur(640, 360, '#10b981')")
        wait_until(52.78)

        # -------------------------------------------------------------
        # SCENE 2 [52.78 -> 84.24s]: Bhashini Voice & Real-Time APIs (Rule 4)
        # -------------------------------------------------------------
        print("[0:53] SCENE 2: Bhashini Multilingual Voice Rails & FastMCP Live APIs...")
        page.evaluate("setHud('🗣️ SCENE 2: Bhashini Voice Ingestion & FastMCP Live Telemetry (Rule 4 Zero Mock Data)')")
        page.evaluate("window.scrollTo({top: 150, behavior: 'smooth'})")

        # Move to Marathi Trigger Button
        page.evaluate("moveCur(420, 275, '#f59e0b')")
        time.sleep(2)

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
        page.evaluate("setHud('🗣️ SCENE 2: Bhashini Voice Ingestion & FastMCP Live Telemetry (Rule 4 Zero Mock Data)')")
        page.evaluate("moveCur(600, 390, '#10b981')")
        wait_until(70)

        # Click English button
        for i in range(buttons.count()):
            try:
                txt = buttons.nth(i).inner_text()
                if "English" in txt:
                    buttons.nth(i).click()
                    break
            except Exception:
                pass

        inject_helpers(page)
        page.evaluate("setHud('🗣️ SCENE 2: Bhashini Voice Ingestion & FastMCP Live Telemetry (Rule 4 Zero Mock Data)')")
        page.evaluate("moveCur(640, 360, '#10b981')")
        wait_until(84.24)

        # -------------------------------------------------------------
        # SCENE 3 [84.24 -> 103.37s]: Meteorological Radar & Chronos-2 Quantiles
        # -------------------------------------------------------------
        print("[1:24] SCENE 3: Open-Meteo Meteorological Radar & Chronos-2 Price Fan Chart...")
        page.evaluate("setHud('🌧️ SCENE 3: Open-Meteo Weather Radar & Chronos-2 Quantile Price Forecasting')")
        page.evaluate("window.scrollTo({top: 480, behavior: 'smooth'})")
        page.evaluate("moveCur(640, 280, '#38bdf8')")
        wait_until(94)

        page.evaluate("window.scrollTo({top: 1600, behavior: 'smooth'})")
        page.evaluate("moveCur(640, 400, '#a855f7')")
        wait_until(103.37)

        # -------------------------------------------------------------
        # SCENE 4 [103.37 -> 140.52s]: Surat False Arbitrage & Arrhenius Q10 Rot
        # -------------------------------------------------------------
        print("[1:43] SCENE 4: 3-Column Arbitrage Matrix & Surat False Arbitrage Trap...")
        page.evaluate("setHud('🔬 SCENE 4: Arrhenius Q10 Decay Physics Exposes the Surat False Arbitrage Trap')")
        page.evaluate("window.scrollTo({top: 720, behavior: 'smooth'})")

        # Point at Option A (Panic sale crash)
        page.evaluate("moveCur(480, 320, '#ef4444')")
        wait_until(115)

        # Point at Option B (Surat Trap - Rot & Diesel)
        page.evaluate("moveCur(800, 320, '#f59e0b')")
        wait_until(128)
        page.evaluate("moveCur(800, 480, '#ef4444')")
        wait_until(140.52)

        # -------------------------------------------------------------
        # SCENE 5 [140.52 -> 188.30s]: WDRA Cold Storage & NABARD Circular 128
        # -------------------------------------------------------------
        print("[2:20] SCENE 5: WDRA Cold Storage + 75% e-NWR Cash Advance (+52% Net Gain)...")
        page.evaluate("setHud('🏛️ SCENE 5: Statutory LightRAG Policy & WDRA e-NWR 75% Pledge Advance (+52% Gain)')")

        # Point at Option C (Recommended)
        page.evaluate("moveCur(1120, 280, '#10b981')")
        wait_until(155)

        # Highlight 75% LTV and Net Gain
        page.evaluate("moveCur(1120, 420, '#10b981')")
        wait_until(170)

        # Scroll to 3D GIS PyDeck Map
        page.evaluate("window.scrollTo({top: 1180, behavior: 'smooth'})")
        page.evaluate("moveCur(640, 450, '#10b981')")
        wait_until(188.30)

        # -------------------------------------------------------------
        # SCENE 6 [188.30 -> 214.36s]: LangGraph Consent Gate & Browser Agent
        # -------------------------------------------------------------
        print("[3:08] SCENE 6: LangGraph Human-in-the-Loop Gate & Automated WDRA Agent...")
        page.evaluate("setHud('⚡ SCENE 6: LangGraph Human-in-the-Loop Consent Gate & Automated WDRA Portal Filing')")
        page.evaluate("window.scrollTo({top: 2750, behavior: 'smooth'})")

        # Point at Consent Gate
        page.evaluate("moveCur(640, 320, '#38bdf8')")
        wait_until(196)

        # Click Approve e-NWR Loan Button
        page.evaluate("moveCur(640, 500, '#10b981')")
        time.sleep(1)
        for i in range(buttons.count()):
            try:
                txt = buttons.nth(i).inner_text()
                if "Approve" in txt or "मंजूर" in txt or "होय" in txt:
                    buttons.nth(i).click()
                    break
            except Exception:
                pass

        inject_helpers(page)
        page.evaluate("setHud('⚡ SCENE 6: Official WDRA Sanction Slip Generated in 1.21s')")
        page.evaluate("window.scrollTo({top: 3100, behavior: 'smooth'})")
        page.evaluate("moveCur(640, 420, '#10b981')")
        wait_until(214.36)

        # -------------------------------------------------------------
        # SCENE 7 [214.36 -> 241.27s]: Real Telemetry, Security Audit & Closing
        # -------------------------------------------------------------
        print("[3:34] SCENE 7: Pan-India APMC Search, AgentShield Grade A & 70/70 Pytests...")
        page.evaluate("setHud('🛡️ SCENE 7: Live Telemetry Search, AgentShield Grade A (100/100) & 70/70 Pytests')")
        page.evaluate("window.scrollTo({top: 2150, behavior: 'smooth'})")

        # Click Fetch Live APMCs to prove live data
        page.evaluate("moveCur(1100, 320, '#10b981')")
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
        page.evaluate("setHud('🛡️ SCENE 7: Live Telemetry Search, AgentShield Grade A (100/100) & 70/70 Pytests')")
        page.evaluate("moveCur(640, 450, '#10b981')")
        wait_until(234)

        # Scroll to Trace inspector and close
        page.evaluate("window.scrollTo({top: 3500, behavior: 'smooth'})")
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

