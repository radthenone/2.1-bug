from app.auth.guard import auth_guard
from flask_restful import Resource, reqparse

from app.auth.service import AuthService
from app.users.schema import UserLoginSchema, UserRegisterSchema


class RegisterController(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("email", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        parser.add_argument("confirm_password", type=str, required=True)
        args = dict(parser.parse_args())

        user_schema = UserRegisterSchema(**args)
        return AuthService.register(user_schema)


class LoginController(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        args = dict(parser.parse_args())

        user_schema = UserLoginSchema(**args)
        return AuthService.login(user_schema)


class LogoutController(Resource):
    @auth_guard()
    def post(self):
        return AuthService.logout()
