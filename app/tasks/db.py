from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import db

if TYPE_CHECKING:
    from app.todos.db import TodoModel


class TaskModel(db.Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    due_date: Mapped[datetime] = mapped_column(nullable=True)
    completed: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # relationship one-to-many
    todo_id: Mapped[int] = mapped_column(ForeignKey("todos.id"), nullable=False)
    todo: Mapped["TodoModel"] = db.relationship("TodoModel", back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.title}>"

    def to_dict(self, fields=None):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "todo_id": self.todo_id,
        }

        if fields:
            return {key: value for key, value in data.items() if key in fields}

        return data
