import time
from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user: Dict) -> Dict[str, str]:
    payload = {
        "id": user["id"],
        "roles": user["roles"],
        "expires": time.time()+60000
    }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    print({**user, "access_token": token})
    return {**user, "access_token": token}


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}