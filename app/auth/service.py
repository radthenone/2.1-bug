from typing import Optional

from flask_restful import abort
from flask_restful import output_json as response
from app.users.schema import UserLoginSchema, UserRegisterSchema

from app.auth.guard import auth_guard
from app.auth.utils import generate_jwt
from app.users.service import UserService


class AuthService:
    @staticmethod
    def authenticate(user_schema: UserLoginSchema) -> Optional[dict]:
        user = UserService.get_user_by_email(user_schema.email)
        if user and UserService.validate_user(user_schema.email, user_schema.password):
            return user.to_dict(fields=["username", "email", "id"])
        return None

    @staticmethod
    def register(user_schema: UserRegisterSchema):
        if UserService.get_user_by_email(user_schema.email):
            abort(400, message="User with this email already exists")

        if UserService.get_user_by_username(user_schema.username):
            abort(400, message="User with this username already exists")

        user = UserService.create_user(
            user_schema.username, user_schema.email, user_schema.password
        )
        if user:
            return response({"message": "User created successfully"}, 201)
        else:
            abort(500, message="Failed to create user")

    @staticmethod
    def login(user_schema: UserLoginSchema):
        user_data = AuthService.authenticate(user_schema)
        if not isinstance(user_data, dict):
            abort(500, message="User data is not a valid dict")

        if not user_data:
            abort(401, message="Wrong username or password")

        access_token = generate_jwt(user_data)
        return response(
            {"message": "Successfully logged in"},
            200,
            {"Authorization": f"Bearer {access_token}"},
        )

    @staticmethod
    @auth_guard()
    def logout():
        return response(
            {"message": "Successfully logged out"}, 200, {"Authorization": None}
        )
