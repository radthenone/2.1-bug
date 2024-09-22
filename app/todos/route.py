from auth.guard import auth_guard, get_user_id
from flask_restful import Resource, abort, reqparse

from app.todos.schema import TodoCreateSchema
from app.todos.service import TodoService
from app.users.service import UserService


class TodoController(Resource):
    @auth_guard()
    def get(self, todo_id=None):
        user_id = get_user_id()
        if todo_id:
            return TodoService.get_todo_by_id(todo_id, user_id)
        abort(404, message="Todo not found")

    @auth_guard()
    def post(self):
        user_id = get_user_id()
        print(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        args = dict(parser.parse_args())

        todo_schema = TodoCreateSchema(name=args["name"], user_id=user_id)

        return TodoService.create_todo(todo_schema)

    @auth_guard()
    def put(self, todo_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        args = parser.parse_args()

        updated_todo = TodoService.update_todo(todo_id, args["name"])
        return updated_todo.to_dict()

    @auth_guard()
    def delete(self, todo_id):
        return TodoService.delete_todo(todo_id)
