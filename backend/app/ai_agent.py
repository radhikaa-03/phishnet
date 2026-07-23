import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


async def analyze_threat(screenshot_b64: str, vt_stats: dict, email_text: str) -> str:
    """
    Analyzes threat using Groq (LLaMA 3) based on VirusTotal stats and email text.
    """
    try:
        prompt = f"""You are a senior cybersecurity analyst specializing in phishing detection.
You have been given two pieces of evidence to analyze:

1. VirusTotal threat intelligence stats: {vt_stats}
2. Suspicious email body (if provided): {email_text if email_text else "No email text provided"}

Analyze all evidence carefully and produce a structured threat report in markdown format with exactly these three sections:

## Verdict
State clearly: SAFE, SUSPICIOUS, or MALICIOUS.
Give a one sentence summary of your conclusion.

## Risk Breakdown
List specific red flags you identified such as:
- VirusTotal vendor flags (malicious count)
- Deceptive or urgent language in the email
- Suspicious claims (asking for payment, fake job offers, etc.)
- Any other red flags

## Educational Takeaway
In simple language a non-technical person can understand, explain:
- What phishing technique was used (if any)
- How to spot this kind of attack in real life
- What the user should do if they received this email or link

Be concise, clear, and professional."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI analysis failed: {str(e)}"