"""
Test script to verify smooth DOM cursor and HUD banner injection in Playwright.
"""
from playwright.sync_api import sync_playwright
import time

def test_hud():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto("http://127.0.0.1:8501", wait_until="domcontentloaded")
        time.sleep(3)

        # Inject HUD and Animated Cursor
        page.evaluate("""
            () => {
                // HUD Banner
                const hud = document.createElement('div');
                hud.id = 'demo-hud-banner';
                hud.style.position = 'fixed';
                hud.style.top = '12px';
                hud.style.left = '50%';
                hud.style.transform = 'translateX(-50%)';
                hud.style.backgroundColor = 'rgba(15, 23, 42, 0.92)';
                hud.style.color = '#38bdf8';
                hud.style.border = '1px solid #0284c7';
                hud.style.padding = '8px 24px';
                hud.style.borderRadius = '30px';
                hud.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
                hud.style.fontSize = '14px';
                hud.style.fontWeight = '700';
                hud.style.boxShadow = '0 10px 25px -5px rgba(0,0,0,0.5)';
                hud.style.zIndex = '9999999';
                hud.style.letterSpacing = '0.5px';
                hud.innerText = '🌾 SCENE 1: The October 2026 Monsoon Glut in Nashik';
                document.body.appendChild(hud);

                // Cursor Pointer
                const cur = document.createElement('div');
                cur.id = 'demo-virtual-cursor';
                cur.style.position = 'fixed';
                cur.style.width = '24px';
                cur.style.height = '24px';
                cur.style.border = '2px solid #ef4444';
                cur.style.borderRadius = '50%';
                cur.style.backgroundColor = 'rgba(239, 68, 68, 0.35)';
                cur.style.boxShadow = '0 0 12px #ef4444';
                cur.style.pointerEvents = 'none';
                cur.style.zIndex = '9999998';
                cur.style.transition = 'all 0.2s cubic-bezier(0.25, 1, 0.5, 1)';
                cur.style.left = '640px';
                cur.style.top = '360px';
                document.body.appendChild(cur);

                window.setDemoHud = (text) => {
                    const el = document.getElementById('demo-hud-banner');
                    if (el) el.innerText = text;
                };

                window.moveDemoCursor = (x, y) => {
                    const el = document.getElementById('demo-virtual-cursor');
                    if (el) {
                        el.style.left = (x - 12) + 'px';
                        el.style.top = (y - 12) + 'px';
                    }
                };
            }
        """)

        # Take test screenshot
        page.screenshot(path="docs/demo_recording/test_hud_screenshot.png")
        print("HUD and cursor injected successfully.")
        browser.close()

if __name__ == "__main__":
    test_hud()

