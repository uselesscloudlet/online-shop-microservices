import time
import jwt
import os
from typing import Dict


JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')

def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_email: str) -> Dict[str, str]:
    payload = {
        "user_email": user_email,
        "expires": time.time() + 200000
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        print(e)
        return {}
