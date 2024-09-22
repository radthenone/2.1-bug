from dataclasses import fields

from flask_restful import abort
from flask_restful import output_json as response

from app.database import db
from app.tasks.db import TaskModel
from app.todos.db import TodoModel
from app.todos.repo import TodoRepository
from app.todos.schema import TodoCreateSchema
from app.users.repo import UserRepository
from app.users.service import UserService


class TodoService:
    @staticmethod
    def exists_todo(todo_name: str, user_id: int) -> bool:
        todo = TodoRepository.get_todo_by_id_and_user(todo_name, user_id)
        if todo:
            return True
        return False

    @staticmethod
    def create_todo(todo_schema: TodoCreateSchema) -> TodoModel:
        user = UserRepository.get_user_by_id(todo_schema.user_id)
        if not user:
            abort(404, message="User not found")

        if TodoService.exists_todo(todo_schema.name, todo_schema.user_id):
            abort(400, message="Todo already exists")

        new_todo = TodoModel(name=todo_schema.name, user_id=todo_schema.user_id)
        db.session.add(new_todo)
        db.session.commit()
        if new_todo:
            return response(
                {"message": f"Todo {new_todo.name} created successfully"}, 201
            )

        abort(500, message="Failed to create todo")

    @staticmethod
    def get_todo_by_id(todo_id: int, user_id: int) -> TodoModel:
        todo = TodoModel.query.filter_by(id=todo_id, user_id=user_id).first()
        if not todo:
            abort(404, message="Todo not found")
        todo_data = todo.to_dict(fields=["id", "name", "user_id"])
        return response(todo_data, 200)

    @staticmethod
    def get_todos_by_user(user_id: int):
        return TodoModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update_todo(todo_id: int, name: str):
        todo = TodoService.get_todo_by_id(todo_id)
        todo.name = name
        db.session.commit()
        return todo

    @staticmethod
    def delete_todo(todo_id: int):
        todo = TodoService.get_todo_by_id(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return response({"message": "Todo deleted successfully"}, 200)
