from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.auth import verify_token

app = FastAPI(title="phishnet API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str
    email_text: str = ""  

# confirms that server is running
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "phishnet API is running"}


# main analysis route 
@app.post("/analyze")
async def analyze(
    request: AnalyzeRequest,
    user=Depends(verify_token)  # auth runs automatically before this function body
):
    
    uid = user.get("uid")
    email = user.get("email")


    screenshot_b64 = "placeholder_screenshot"
    vt_stats = {"malicious": 0, "suspicious": 0, "harmless": 0}
    ai_report = "AI analysis not yet connected"

    return {
        "user": email,
        "url_analyzed": request.url,
        "screenshot_taken": True,
        "vt_stats": vt_stats,
        "report": ai_report
    }