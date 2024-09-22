from http.client import responses

from flask_restful import Resource, abort, reqparse
from flask_restful import output_json as response

from app.auth.guard import auth_guard, get_user_id
from app.tasks.schema import TaskCreateSchema, TaskUpdateSchema
from app.tasks.service import TaskService
from app.todos.service import TodoService


class TestController(Resource):
    def get(self, task_id=None):
        if task_id:
            task = TaskService.get_task_by_id(task_id)
            if not task:
                abort(404, message=f"Task with ID {task_id} not found")
            return response(
                task.to_dict(
                    fields=["id", "title", "description", "due_date", "completed"]
                ),
                code=200,
                headers={"Content-Type": "application/json"},
            )

        abort(400, message="task_id must be provided")


class TaskController(Resource):
    @auth_guard()
    def get(self, todo_id=None, task_id=None):
        if todo_id:
            return TaskService.get_tasks_by_todo_id(todo_id)
        if task_id:
            return TaskService.get_task_by_id(task_id)
        abort(400, message="Either todo_id or task_id must be provided")

    @auth_guard()
    def post(self, todo_id=None):
        TodoService.provided_todo_id(todo_id, get_user_id())

        parser = reqparse.RequestParser()
        parser.add_argument(
            "title", type=str, required=True, help="Title cannot be blank"
        )
        parser.add_argument("description", type=str, required=False)
        parser.add_argument("due_date", type=str, required=False)
        args = dict(parser.parse_args())
        try:
            task_schema = TaskCreateSchema(**args)
            return TaskService.create_task(
                todo_id=todo_id,
                task_schema=task_schema,
            )
        except Exception as e:
            abort(400, message=str(e))

    @auth_guard()
    def put(self, task_id):
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True)
        parser.add_argument("description", type=str, required=False)
        parser.add_argument("due_date", type=str, required=False)
        parser.add_argument("completed", type=bool, required=False)
        args = dict(parser.parse_args())

        task = TaskService.get_task_by_id_completed(task_id)
        if not task:
            abort(404, message="Task not found")
        try:
            task_update_schema = TaskUpdateSchema(**args)
            return TaskService.update_task(
                task=task,
                task_update_schema=task_update_schema,
            )
        except Exception as e:
            abort(400, message=str(e))

    @auth_guard()
    def delete(self, task_id):
        return TaskService.delete_task(task_id)
