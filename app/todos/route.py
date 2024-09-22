from flask_restful import Resource, reqparse

from app.auth.guard import auth_guard, get_user_id
from app.todos.schema import TodoCreateSchema, TodoUpdateSchema
from app.todos.service import TodoService


class TodoController(Resource):
    @auth_guard()
    def get(self, todo_id=None):
        user_id = get_user_id()
        if todo_id:
            return TodoService.get_todo_by_id(todo_id, user_id)
        else:
            return TodoService.get_todos_by_user(user_id)

    @auth_guard()
    def post(self):
        user_id = get_user_id()
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        args = dict(parser.parse_args())

        todo_schema = TodoCreateSchema(name=args["name"], user_id=user_id)

        return TodoService.create_todo(todo_schema)

    @auth_guard()
    def put(self, todo_id=None):
        user_id = get_user_id()
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        args = dict(parser.parse_args())

        todo_schema = TodoUpdateSchema(name=args["name"])

        return TodoService.update_todo(todo_id, user_id, todo_schema)

    @auth_guard()
    def delete(self, todo_id):
        user_id = get_user_id()
        return TodoService.delete_todo(todo_id, user_id)
