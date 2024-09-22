from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column

from app.database import db

if TYPE_CHECKING:
    from app.todos.db import TodoModel


class UserModel(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # relationships many-to-one
    todos: Mapped[List["TodoModel"]] = db.relationship(
        "TodoModel", back_populates="user"
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self, fields=None):
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "todos": [todo.to_dict() for todo in self.todos],
        }

        if fields:
            return {key: value for key, value in data.items() if key in fields}

        return data
