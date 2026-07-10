import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.web_worker import take_screenshot
from app.ai_agent import analyze_threat

async def test():
    print("Taking screenshot...")
    screenshot_b64 = await take_screenshot("https://xyz.com")
    print("Screenshot taken. Sending to Gemini for evaluation.....")

    vt_stats = {"malicious": 0, "suspicious": 0, "harmless": 70, "undetected": 20}
    email_text = "Your account has been suspended. Click here immediately to verify."

    report = await analyze_threat(screenshot_b64, vt_stats, email_text)
    print("\n------ THREAT REPORT ------")
    print(report)

asyncio.run(test())