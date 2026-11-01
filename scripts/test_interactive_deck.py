import asyncio
import os
from playwright.async_api import async_playwright

async def test_deck():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        
        file_path = os.path.abspath("docs/PITCH_DECK.html")
        file_url = f"file:///{file_path.replace(os.sep, '/')}"
        print(f"Opening {file_url}...")
        await page.goto(file_url)
        
        # Verify title
        title = await page.title()
        print(f"Page title: {title}")
        assert "KrishiArtha-MCP" in title
        
        # Verify Slide 1 active
        s1 = await page.query_selector("#slide-1.active")
        assert s1 is not None, "Slide 1 should be active initially"
        print("Slide 1 is active.")
        
        # Test keyboard navigation: ArrowRight to Slide 2
        await page.keyboard.press("ArrowRight")
        await asyncio.sleep(0.4)
        s2 = await page.query_selector("#slide-2.active")
        assert s2 is not None, "Slide 2 should be active after ArrowRight"
        print("ArrowRight navigated to Slide 2.")
        
        # Test keyboard navigation: Space to Slide 3
        await page.keyboard.press("Space")
        await asyncio.sleep(0.4)
        s3 = await page.query_selector("#slide-3.active")
        assert s3 is not None, "Slide 3 should be active after Space"
        print("Space navigated to Slide 3.")
        
        # Test keyboard navigation: Direct digit jump '5' to Slide 5
        await page.keyboard.press("5")
        await asyncio.sleep(0.4)
        s5 = await page.query_selector("#slide-5.active")
        assert s5 is not None, "Slide 5 should be active after pressing '5'"
        print("Digit '5' navigated to Slide 5.")
        
        # Check text on Slide 5
        text_5 = await s5.inner_text()
        assert "68,400" in text_5, "Slide 5 should feature ₹68,400 net realization"
        assert "5,600" in text_5, "Slide 5 should feature itemized ₹5,600 storage deduction"
        print("Slide 5 verified with ₹68,400 and ₹5,600 deduction.")
        
        # Test Jump to Slide 9
        await page.keyboard.press("9")
        await asyncio.sleep(0.4)
        s9 = await page.query_selector("#slide-9.active")
        assert s9 is not None, "Slide 9 should be active after pressing '9'"
        print("Digit '9' navigated to Slide 9.")
        
        # Take a screenshot of Slide 9
        os.makedirs("scripts/test_output", exist_ok=True)
        await page.screenshot(path="scripts/test_output/slide_9_screenshot.png")
        print("Saved screenshot of Slide 9.")

        # Test Jump to Slide 1
        await page.keyboard.press("Home")
        await asyncio.sleep(0.4)
        s1_again = await page.query_selector("#slide-1.active")
        assert s1_again is not None, "Slide 1 should be active after Home key"
        print("Home key navigated back to Slide 1.")

        await page.screenshot(path="scripts/test_output/slide_1_screenshot.png")
        print("Saved screenshot of Slide 1.")

        # Test clicking slide dot 4 (Slide 4)
        dots = await page.query_selector_all(".slide-dot")
        assert len(dots) == 9, f"Expected 9 dots, got {len(dots)}"
        await dots[3].click()
        await asyncio.sleep(0.4)
        s4 = await page.query_selector("#slide-4.active")
        assert s4 is not None, "Slide 4 should be active after clicking dot 4"
        print("Clicking dot 4 successfully navigated to Slide 4.")
        
        await page.screenshot(path="scripts/test_output/slide_4_screenshot.png")
        print("Saved screenshot of Slide 4.")

        await browser.close()
        print("All interactive deck tests PASSED!")

asyncio.run(test_deck())
