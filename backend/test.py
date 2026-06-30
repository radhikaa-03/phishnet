import asyncio
from playwright.async_api import async_playwright

async def take_screenshot():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        await page.screenshot(path="test_screenshot.png")
        await browser.close()
        print("Screenshot saved successfully!")

asyncio.run(take_screenshot())