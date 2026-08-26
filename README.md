# phishnet 

A phishing detection tool- You paste a suspicious URL or a sketchy email you received, and it tells you whether it's safe, suspicious, or malicious — and explains why

---

## how it works

1. sign in with google
2. paste the suspicious URL and/or the email body
3. the backend does three things at once:
   - opens a headless chrome browser, visits the URL, takes a screenshot
   - checks the URL against 90+ antivirus vendors via VirusTotal
   - sends the screenshot + VT results + email text to an LLM
4. the AI looks at everything and gives you a proper threat report

---

## live demo
frontend → https://phishnet-delta.vercel.app  
backend → https://phishnet-vbqi.onrender.com

---

## stack

- **frontend** — Next.js + Tailwind CSS
- **backend** — FastAPI (Python)
- **auth** — Firebase + JWT verification
- **browser automation** — Playwright 
- **threat intel** — VirusTotal API v3
- **AI** — Groq API (LLaMA 3.3 70B)
- **containerization** — Docker

everything except Docker is free tier. no credit card needed to run this locally.

---

## project structure

```
phishnet/
├── backend/
│   ├── app/
│   │   ├── main.py          # fastapi server + routes
│   │   ├── auth.py          # firebase token verification
│   │   ├── web_worker.py    # playwright screenshot logic
│   │   ├── intel_worker.py  # virustotal integration
│   │   └── ai_agent.py      # groq llm threat analysis
│   ├── scratch/             # standalone test scripts i used while building
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── app/
    │   ├── page.tsx         # main dashboard
    │   └── firebase.js      # firebase client init
    └── .env.local.example
```

---

## running locally

**backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # windows
pip install -r requirements.txt
playwright install chromium
uvicorn app.main:app --reload --loop asyncio
```

you'll need a `.env` file:
```
FIREBASE_SERVICE_ACCOUNT_PATH=./app/service-account.json
VIRUSTOTAL_API_KEY=your_key
GROQ_API_KEY=your_key
```

get VirusTotal key free at virustotal.com, Groq key free at console.groq.com

**frontend:**
```bash
cd frontend
npm install
npm run dev
```

fill in `.env.local` with your Firebase web config (from Firebase console → project settings)

---

