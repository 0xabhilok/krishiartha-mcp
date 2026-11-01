import asyncio
import os
from playwright.async_api import async_playwright

async def screenshot_all_slides():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        
        file_path = os.path.abspath("docs/PITCH_DECK.html")
        file_url = f"file:///{file_path.replace(os.sep, '/')}"
        await page.goto(file_url)
        
        out_dir = "scripts/test_output/deck_slides"
        os.makedirs(out_dir, exist_ok=True)
        
        dots = await page.query_selector_all(".slide-dot")
        for i in range(9):
            await dots[i].click()
            await asyncio.sleep(0.3)
            shot_path = os.path.join(out_dir, f"slide_{i+1}.png")
            await page.screenshot(path=shot_path)
            print(f"Captured Slide {i+1} -> {shot_path}")
            
        await browser.close()
        print("Captured all 9 slides!")

asyncio.run(screenshot_all_slides())
