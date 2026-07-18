import base64
import asyncio
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright

executor = ThreadPoolExecutor(max_workers=2)


def _take_screenshot_sync(url: str) -> str:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.goto(url, timeout=15000, wait_until="domcontentloaded")
            screenshot_bytes = page.screenshot(full_page=True)
            return base64.b64encode(screenshot_bytes).decode("utf-8")
        finally:
            browser.close()


async def take_screenshot(url: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _take_screenshot_sync, url)