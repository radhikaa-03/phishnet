import asyncio
import sys
sys.path.append("..") 
from app.web_worker import take_screenshot

async def test():
    print("Screenshotting..")
    result = await take_screenshot("https://abc.com")
    print(f"Success! Base64 string length: {len(result)} characters")
    print(f"First 100 chars: {result[:100]}")

asyncio.run(test())