import logging
from typing import Optional

from app.database import db
from app.todos.db import TodoModel
from app.todos.schema import TodoCreateSchema, TodoUpdateSchema


class TodoRepository:
    @staticmethod
    def get_todo_by_id(todo_id: int) -> Optional[TodoModel]:
        return TodoModel.query.filter_by(id=todo_id).first()

    @staticmethod
    def get_todo_by_name_and_user(todo_name: str, user_id: int) -> TodoModel:
        return TodoModel.query.filter_by(name=todo_name, user_id=user_id).first()

    @staticmethod
    def get_todo_by_id_and_user(todo_id: int, user_id: int) -> TodoModel:
        return TodoModel.query.filter_by(id=todo_id, user_id=user_id).first()

    @staticmethod
    def get_todos_by_user(user_id: int) -> list[TodoModel]:
        return TodoModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_todo(todo_schema: TodoCreateSchema) -> Optional[TodoModel]:
        new_todo = TodoModel(name=todo_schema.name, user_id=todo_schema.user_id)
        db.session.add(new_todo)
        db.session.commit()
        if new_todo:
            return new_todo
        return None

    @staticmethod
    def update_todo(
        todo_id: int, user_id: int, todo_schema: TodoUpdateSchema
    ) -> TodoModel:
        todo = TodoRepository.get_todo_by_id_and_user(todo_id, user_id)
        todo.name = todo_schema.name
        db.session.commit()
        return todo

    @staticmethod
    def delete_todo(todo_id: int, user_id: int) -> bool:
        try:
            todo = TodoRepository.get_todo_by_id_and_user(todo_id, user_id)
            db.session.delete(todo)
            db.session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False
