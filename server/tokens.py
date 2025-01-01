import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

def create_token(id):
    payload = {
        "user_id" : id,
        "iat" : datetime.now(timezone.utc),
        "exp" : datetime.now(timezone.utc) + timedelta(hours=1),
    }
    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
    return token

def decrypt_token(encoded)->dict:
    try:
        this_payload = jwt.decode(encoded, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        return {"Valid" : True, "payload" : this_payload}
    except jwt.ExpiredSignatureError:
        return {"Valid" : False, "error" : "Token has expired."}
    except jwt.InvalidTokenError:
        return {"Valid" : False, "error" : "Token is invalid."}
    
def get_user_id(payload: dict)->int:
    return payload.get("user_id")