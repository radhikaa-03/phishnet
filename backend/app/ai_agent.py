import os
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini client 
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


async def analyze_threat(screenshot_b64: str, vt_stats: dict, email_text: str) -> str:
    """
    Takes a Base64 screenshot, VirusTotal stats, and email text.
    Sends everything to Gemini and returns a structured markdown threat report.
    """

    try:
        # Convert Base64 back to raw bytes
        screenshot_bytes = base64.b64decode(screenshot_b64)

        # Build the prompt
        prompt = f"""
You are a senior cybersecurity analyst specializing in phishing detection.
You have been given three pieces of evidence to analyze:

1. A screenshot of a suspicious website (attached as image)
2. VirusTotal threat intelligence stats: {vt_stats}
3. A suspicious email body (if provided): {email_text if email_text else "No email text provided"}

Analyze all evidence carefully and produce a structured threat report in markdown format with exactly these three sections:

***Verdict
State clearly: SAFE, SUSPICIOUS, or MALICIOUS.
Give a one sentence summary of your conclusion.

***Risk Breakdown
List specific red flags you identified such as:
- Brand impersonation (fake logos, cloned UI)
- Deceptive or urgent language
- Credential harvesting forms
- Mismatch between email claims and actual website
- VirusTotal vendor flags
- Suspicious URL patterns

***Educational Takeaway
In simple language a non-technical person can understand, explain:
- What phishing technique was used (if any)
- How to spot this kind of attack in real life
- What the user should do if they received this email or link

Be concise, clear, and professional.
"""

        # Send image + text together to Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=screenshot_bytes, mime_type="image/png"),
                prompt
            ]
        )

        return response.text

    except Exception as e:
        return f"AI analysis failed: {str(e)}"