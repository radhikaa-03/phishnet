import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
BASE_URL = "https://www.virustotal.com/api/v3"

HEADERS = {
    "x-apikey": VIRUSTOTAL_API_KEY
}


def check_virustotal(url: str) -> dict:


    try:
        #submit url for scanning
        response = requests.post(
            f"{BASE_URL}/urls",
            headers=HEADERS,
            data={"url": url}
        )
        response.raise_for_status()
        analysis_id = response.json()["data"]["id"]

	#while it scans
        time.sleep(3)

        result = requests.get(
            f"{BASE_URL}/analyses/{analysis_id}",
            headers=HEADERS
        ) #analysis results
        result.raise_for_status()

        stats = result.json()["data"]["attributes"]["stats"]

        return {
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0),
            "undetected": stats.get("undetected", 0)
        }

    except Exception as e:
        print(f"VirusTotal error: {str(e)}")
        return {
            "malicious": 0,
            "suspicious": 0,
            "harmless": 0,
            "undetected": 0
        }