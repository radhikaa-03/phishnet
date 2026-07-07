import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.intel_worker import check_virustotal

print("Checking URL using Virustotal......")
result = check_virustotal("http://malware.testing.google.test/testing/malware/")
print(f"Results: {result}")