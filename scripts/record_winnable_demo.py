"""
Record Winnable 4-Minute Demo Video Synchronized with World-Class Neural Narration.
Drives the live Streamlit cockpit (100% live APIs, Rule 4 compliant).
"""
import time
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path("docs/demo_recording")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def record():
    # Remove previous webm
    for f in OUTPUT_DIR.glob("*.webm"):
        try:
            f.unlink()
        except Exception:
            pass

    with sync_playwright() as p:
        print("[0:00] Launching browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir=str(OUTPUT_DIR),
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()

        print("[0:05] Navigating to live prototype on http://127.0.0.1:8501...")
        page.goto("http://127.0.0.1:8501", wait_until="domcontentloaded", timeout=25000)
        time.sleep(5)

        # [0:10 - 0:50] Segment 1: Hook & Crisis (40s)
        print("[0:10] Showing Cockpit Header, Live Status Badge & Crisis Context...")
        time.sleep(38)

        # [0:50 - 1:25] Segment 2: Bhashini Voice & Real APIs (35s)
        print("[0:50] Clicking Marathi Voice Trigger & Bhashini ASR Slot Extraction...")
        buttons = page.locator("button")
        for i in range(buttons.count()):
            try:
                txt = buttons.nth(i).inner_text()
                if "मराठी" in txt:
                    buttons.nth(i).click()
                    time.sleep(4)
                    break
            except Exception:
                pass

        time.sleep(12)

        for i in range(buttons.count()):
            try:
                txt = buttons.nth(i).inner_text()
                if "English" in txt:
                    buttons.nth(i).click()
                    time.sleep(3)
                    break
            except Exception:
                pass

        time.sleep(12)

        # [1:25 - 1:50] Segment 3: Live Weather Radar & Chronos-2 (25s)
        print("[1:25] Scrolling to Meteorological Radar (Open-Meteo) & Chronos-2 Fan Chart...")
        page.evaluate("window.scrollTo({top: 450, behavior: 'smooth'})")
        time.sleep(12)
        page.evaluate("window.scrollTo({top: 1550, behavior: 'smooth'})")
        time.sleep(12)

        # [1:50 - 2:30] Segment 4: 3-Column Arbitrage Matrix & Surat Decay Physics (40s)
        print("[1:50] Scrolling to 3-Column Arbitrage Matrix & Arrhenius Q10 Decay...")
        page.evaluate("window.scrollTo({top: 720, behavior: 'smooth'})")
        time.sleep(38)

        # [2:30 - 3:20] Segment 5: WDRA Option C & 3D GIS Map (50s)
        print("[2:30] Highlighting Option C WDRA Cold Storage & 3D GIS Route Simulator...")
        time.sleep(25)
        page.evaluate("window.scrollTo({top: 1150, behavior: 'smooth'})")
        time.sleep(22)

        # [3:20 - 3:45] Segment 6: LangGraph HITL Consent Gate & Browser Agent (25s)
        print("[3:20] LangGraph Consent Gate: Clicking 'Approve e-NWR Loan'...")
        page.evaluate("window.scrollTo({top: 2750, behavior: 'smooth'})")
        time.sleep(4)

        for i in range(buttons.count()):
            try:
                txt = buttons.nth(i).inner_text()
                if "Approve" in txt or "मंजूर" in txt or "होय" in txt:
                    buttons.nth(i).click()
                    time.sleep(5)
                    break
            except Exception:
                pass

        time.sleep(16)

        # [3:45 - 4:02] Segment 7: Official Sanction Slip, Rule 4 Audit & Closing (17s)
        print("[3:45] Viewing WDRA Sanction Slip & National Scale Summary...")
        page.evaluate("window.scrollTo({top: 3400, behavior: 'smooth'})")
        time.sleep(15)

        print("[4:02] Closing recording context...")
        context.close()
        browser.close()
        print("Browser recording complete.")

    # Find the recorded webm
    webm_files = list(OUTPUT_DIR.glob("*.webm"))
    if not webm_files:
        print("ERROR: No webm file found!")
        return

    latest_webm = max(webm_files, key=lambda f: f.stat().st_mtime)
    print(f"Recorded webm: {latest_webm}")

    narration_audio = Path("docs/demo_recording/world_class_narration.mp3")
    final_mp4 = Path("docs/KrishiArtha_MCP_Winnable_5Min_Demo.mp4")

    print(f"Merging video and neural narration into {final_mp4} using FFmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(latest_webm),
        "-i", str(narration_audio),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(final_mp4)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"SUCCESS: Winnable demo video generated at {final_mp4} (Size: {final_mp4.stat().st_size} bytes)")
    else:
        print(f"FFmpeg error: {res.stderr}")

if __name__ == "__main__":
    record()

