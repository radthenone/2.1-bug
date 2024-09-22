from auth.guard import auth_guard
from flask_restful import Resource, reqparse
from tasks.service import TaskService


class TaskController(Resource):
    @auth_guard()
    def get(self, task_id=None, todo_id=None):
        if task_id:
            return TaskService.get_task_by_id(task_id).to_dict()

        tasks = TaskService.get_tasks_by_todo_id(todo_id)
        return [task.to_dict() for task in tasks]

    @auth_guard()
    def post(self, todo_id):
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True)
        parser.add_argument("description", type=str, required=False)
        parser.add_argument("due_date", type=str, required=False)
        args = parser.parse_args()

        new_task = TaskService.create_task(
            todo_id=todo_id,
            title=args["title"],
            description=args.get("description"),
            due_date=args.get("due_date"),
        )
        return new_task.to_dict(), 201

    @auth_guard()
    def put(self, task_id):
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True)
        parser.add_argument("description", type=str, required=False)
        parser.add_argument("due_date", type=str, required=False)
        parser.add_argument("completed", type=bool, required=False)
        args = parser.parse_args()

        updated_task = TaskService.update_task(
            task_id=task_id,
            title=args["title"],
            description=args.get("description"),
            due_date=args.get("due_date"),
            completed=args.get("completed"),
        )
        return updated_task.to_dict()

    @auth_guard()
    def delete(self, task_id):
        return TaskService.delete_task(task_id)
