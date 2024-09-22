from flask import request
from flask_restful import abort

from app.auth.utils import decode_jwt


def check_jwt():
    token = request.headers.get("Authorization")
    if not token:
        abort(401, message="Missing Authorization token")
    jwt_token = token.split("Bearer ")[1]
    try:
        return decode_jwt(jwt_token)
    except Exception:
        abort(401, message="Invalid Authorization token")


def get_user_id():
    token = request.headers.get("Authorization")
    if not token:
        abort(401, message="Missing Authorization token")
    jwt_token = token.split("Bearer ")[1]
    return decode_jwt(jwt_token)["id"]


def auth_guard():
    def wrapper(route_function):
        def decorated_function(*args, **kwargs):
            try:
                check_jwt()
            except Exception as e:
                abort(401, message=str(e))
            return route_function(*args, **kwargs)

        decorated_function.__name__ = route_function.__name__
        return decorated_function

    return wrapper
