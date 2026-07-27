import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.auth import verify_token
from app.web_worker import take_screenshot
from app.intel_worker import check_virustotal
from app.ai_agent import analyze_threat

app = FastAPI(title="phishnet API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://phishnet-delta.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    url: str
    email_text: str = ""


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "phishnet API is running successfully"}


@app.post("/analyze")
async def analyze(
    request: AnalyzeRequest,
    user=Depends(verify_token)
):
    email = user.get("email")

    screenshot_b64 = await take_screenshot(request.url)
    vt_stats = check_virustotal(request.url)
    report = await analyze_threat(screenshot_b64, vt_stats, request.email_text)

    return {
        "user": email,
        "url_analyzed": request.url,
        "vt_stats": vt_stats,
        "report": report
    }