import os
from datetime import datetime, timedelta

import jwt


def generate_jwt(payload, lifetime=None):
    if lifetime:
        payload["exp"] = (datetime.now() + timedelta(minutes=lifetime)).timestamp()
    return jwt.encode(payload, os.environ.get("SECRET_KEY", "dev"), algorithm="HS256")


def decode_jwt(token):
    return jwt.decode(token, os.environ.get("SECRET_KEY", "dev"), algorithms=["HS256"])
