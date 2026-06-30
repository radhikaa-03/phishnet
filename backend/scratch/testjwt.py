import jwt
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlJhZGhpa2EiLCJyb2xlIjoiaXQgc3R1ZGVudCJ9.oT5t0AeM_GondPYnp6MO-aPqy4sS9E9riXfIpAGihv8"
secret = "a-string-secret-at-least-256-bits-long"
#without verification
unverified = jwt.decode(token, options={"verify_signature": False})
print("Unverified payload:")
print(unverified)

#with verification
try:
    verified = jwt.decode(token, secret, algorithms=["HS256"])
    print("\nVERIFIED! Payload:")
    print(verified)
except jwt.InvalidSignatureError:
    print("\nVERIFICATION FAILED!! SIGNATURE DOESN'T MATCH!")