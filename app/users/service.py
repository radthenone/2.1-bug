from werkzeug.security import check_password_hash, generate_password_hash

from app.users.db import UserModel
from app.users.repo import UserRepository


class UserService:
    @staticmethod
    def create_user(username: str, email: str, password: str) -> UserModel:
        hashed_password = generate_password_hash(password)
        return UserRepository.create_user(
            username=username, email=email, password=hashed_password
        )

    @staticmethod
    def get_user_by_id(user_id: int) -> UserModel:
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def get_user_by_email(email: str) -> UserModel:
        return UserRepository.get_user_by_email(email)

    @staticmethod
    def get_user_by_username(username: str) -> UserModel:
        return UserRepository.get_user_by_username(username)

    @staticmethod
    def validate_username(username: str) -> bool:
        user = UserRepository.get_user_by_username(username)
        if user:
            return False
        return True

    @staticmethod
    def validate_user(email: str, password: str) -> bool:
        user = UserRepository.get_user_by_email(email)
        if user and check_password_hash(user.password, password):
            return True
        return False
