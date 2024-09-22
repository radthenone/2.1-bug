from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import db

if TYPE_CHECKING:
    from app.tasks.db import TaskModel
    from app.users.db import UserModel


class TodoModel(db.Model):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )

    # relationship one-to-many
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["UserModel"] = db.relationship(back_populates="todos")

    # relationship many-to-one
    tasks: Mapped[List["TaskModel"]] = db.relationship(back_populates="todo")

    def to_dict(self, fields=None):
        data = {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "user_id": self.user_id,
            "tasks": [task.to_dict() for task in self.tasks],
        }

        if fields:
            return {key: value for key, value in data.items() if key in fields}

        return data
