import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Header, HTTPException

cred = credentials.Certificate("app/secret.json")
firebase_admin.initialize_app(cred)


async def verify_token(authorization: str = Header(...)): #checks authorization headers if they start with "Bearer "
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    #remove "Bearer " prefix
    token = authorization.split("Bearer ")[1]

    #firebase verifies if token is eligible
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # contains uid, email, custom claims, etc.
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")