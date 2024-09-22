from werkzeug.security import check_password_hash, generate_password_hash

from app.database import db
from app.users.db import UserModel


class UserRepository:
    @staticmethod
    def create_user(username: str, email: str, password: str) -> UserModel:
        new_user = UserModel(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_user_by_id(user_id: int) -> UserModel:
        return UserModel.query.get(user_id)

    @staticmethod
    def get_user_by_email(email: str) -> UserModel:
        return UserModel.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_username(username: str) -> UserModel:
        return UserModel.query.filter_by(username=username).first()
