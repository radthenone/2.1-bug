from datetime import datetime

from flask_restful import abort
from flask_restful import output_json as response

from app.database import db
from app.tasks.db import TaskModel
from app.todos.db import TodoModel
from app.todos.service import TodoService


class TaskService:
    @staticmethod
    def create_task(
        todo_id: int, title: str, description: str = None, due_date: datetime = None
    ) -> TaskModel:
        todo = TodoService.get_todo_by_id(todo_id)
        if not todo:
            abort(404, message="Todo not found")

        new_task = TaskModel(
            title=title, description=description, due_date=due_date, todo_id=todo_id
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task

    @staticmethod
    def get_task_by_id(task_id: int) -> TaskModel:
        task = TaskModel.query.get(task_id)
        if not task:
            abort(404, message="Task not found")
        return task

    @staticmethod
    def get_tasks_by_todo_id(todo_id: int):
        return TaskModel.query.filter_by(todo_id=todo_id).all()

    @staticmethod
    def update_task(
        task_id: int,
        title: str,
        description: str = None,
        due_date: datetime = None,
        completed: bool = None,
    ):
        task = TaskService.get_task_by_id(task_id)
        task.title = title
        task.description = description
        task.due_date = due_date
        task.completed = completed
        db.session.commit()
        return task

    @staticmethod
    def delete_task(task_id: int):
        task = TaskService.get_task_by_id(task_id)
        db.session.delete(task)
        db.session.commit()
        return response({"message": "Task deleted successfully"}, 200)
