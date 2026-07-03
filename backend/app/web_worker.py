import asyncio
import base64
from playwright.async_api import async_playwright


async def take_screenshot(url: str) -> str:

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    async with async_playwright() as p:
        browser = None
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
            )

            page = await context.new_page()
            await page.goto(url, timeout=15000, wait_until="domcontentloaded")
            screenshot_bytes = await page.screenshot(full_page=True)
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode("utf-8")

            return screenshot_b64

        except Exception as e:
            raise Exception(f"Screenshot failed for {url}: {str(e)}")

        finally:
            if browser:
                await browser.close()