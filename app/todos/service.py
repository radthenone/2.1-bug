from flask_restful import abort
from flask_restful import output_json as response

from app.todos.db import TodoModel
from app.todos.repo import TodoRepository
from app.todos.schema import TodoCreateSchema, TodoUpdateSchema
from app.users.repo import UserRepository


class TodoService:
    @staticmethod
    def provided_todo_id(todo_id: int, user_id: int):
        if not todo_id or todo_id not in [
            todo.id for todo in TodoRepository.get_todos_by_user(user_id=user_id)
        ]:
            abort(400, message="Invalid todo id")

    @staticmethod
    def exists_todo(todo_name: str, user_id: int) -> bool:
        todo = TodoRepository.get_todo_by_name_and_user(todo_name, user_id)
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

        new_todo = TodoRepository.create_todo(todo_schema)
        if new_todo:
            return response(
                {"message": f"Todo {new_todo.name} created successfully"}, 201
            )

        abort(500, message="Failed to create todo")

    @staticmethod
    def get_todo_by_id(todo_id: int, user_id: int) -> TodoModel:
        todo = TodoRepository.get_todo_by_id_and_user(todo_id, user_id)
        if not todo:
            abort(404, message="Todo not found")
        todo_data = todo.to_dict(fields=["id", "name"])
        return response(todo_data, 200)

    @staticmethod
    def get_todos_by_user(user_id: int):
        todos = TodoRepository.get_todos_by_user(user_id)
        if not todos:
            abort(404, message="Todos not found")
        todos_data = [todo.to_dict(fields=["id", "name"]) for todo in todos]
        return response(todos_data, 200)

    @staticmethod
    def update_todo(todo_id: int, user_id: int, todo_schema: TodoUpdateSchema):
        update_todo = TodoRepository.update_todo(
            todo_id=todo_id, user_id=user_id, todo_schema=todo_schema
        )
        if update_todo:
            return response(
                {"message": f"Todo {update_todo.name} updated successfully"}, 201
            )

        abort(500, message="Failed to update todo")

    @staticmethod
    def delete_todo(
        todo_id: int,
        user_id: int,
    ):
        if not TodoRepository.get_todo_by_id(todo_id):
            abort(404, message="Todo not found")
        TodoRepository.delete_todo(todo_id, user_id)
        return response({"message": "Todo deleted successfully"}, 200)
