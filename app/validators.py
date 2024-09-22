import re

from email_validator import EmailNotValidError
from flask_restful import abort


def validate_password(password: str) -> str:
    if len(password) < 8:
        abort(400, message="Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        abort(400, message="Password must contain at least one number")
    if not any(char.isupper() for char in password):
        abort(400, message="Password must contain at least one uppercase letter")
    if not any(char.islower() for char in password):
        abort(400, message="Password must contain at least one lowercase letter")
    if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>/?~" for char in password):
        abort(400, message="Password must contain at least one special character")
    return password


def check_passwords_match(password: str, rewrite_password: str) -> bool:
    if password != rewrite_password:
        abort(400, message="passwords do not match")
    return True


def validate_username(username: str) -> str:
    pattern = r"^[a-zA-Z0-9_-]{3,16}$"
    if not re.match(pattern, username):
        abort(
            400,
            message="username must only contain letters, numbers, dashes and underscores",
        )
    return username


def validate_email(email: str) -> str:
    from email_validator import validate_email

    try:
        validate_email(email)
    except EmailNotValidError as e:
        abort(400, message=str(e))
    return email
