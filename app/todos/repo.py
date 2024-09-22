from typing import Optional

from app.database import db
from app.todos.db import TodoModel
from app.todos.schema import TodoCreateSchema


class TodoRepository:
    @staticmethod
    def get_todo_by_id_and_user(todo_name: str, user_id: int) -> TodoModel:
        return TodoModel.query.filter_by(name=todo_name, user_id=user_id).first()

    @staticmethod
    def create_todo(todo_schema: TodoCreateSchema) -> Optional[TodoModel]:
        new_todo = TodoModel(name=todo_schema.name, user_id=todo_schema.user_id)
        db.session.add(new_todo)
        db.session.commit()
        if new_todo:
            return new_todo
        return None
