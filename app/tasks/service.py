from typing import Optional

from flask_restful import abort
from flask_restful import output_json as response

from app.database import db
from app.tasks.db import TaskModel
from app.tasks.repo import TaskRepository
from app.tasks.schema import TaskCreateSchema, TaskUpdateSchema


class TaskService:
    @staticmethod
    def get_task_by_id(task_id: int):
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            abort(404, message=f"Task with ID {task_id} not found")
        return response(
            task.to_dict(
                fields=["id", "title", "description", "due_date", "completed"]
            ),
            code=200,
            headers={"Content-Type": "application/json"},
        )

    @staticmethod
    def get_tasks_by_todo_id(todo_id: int):
        tasks = TaskRepository.get_tasks_by_todo_id(todo_id)
        if not tasks:
            abort(404, message=f"No tasks found for Todo ID {todo_id}")
        return response(
            [
                task.to_dict(
                    fields=[
                        "id",
                        "title",
                        "description",
                        "due_date",
                        "completed",
                    ]
                )
                for task in tasks
            ],
            code=200,
            headers={"Content-Type": "application/json"},
        )

    @staticmethod
    def create_task(
        todo_id: int,
        task_schema: TaskCreateSchema,
    ):
        if TaskRepository.exists_task(todo_id, task_schema.title):
            abort(409, message="Task already exists")

        new_task = TaskRepository.create_task(
            todo_id=todo_id,
            task_schema=task_schema,
        )
        if new_task:
            return response(
                {
                    "message": "Task created successfully",
                    "task": new_task.to_dict(
                        fields=[
                            "id",
                            "title",
                            "description",
                            "due_date",
                            "completed",
                        ]
                    ),
                },
                201,
            )
        abort(500, message="Failed to create task")

    @staticmethod
    def get_task_by_id_completed(task_id: int) -> Optional[TaskModel]:
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            abort(404, message="Task not found")
        if task.completed:
            abort(400, message="Task is already completed")
        return task

    @staticmethod
    def update_task(
        task: TaskModel,
        task_update_schema: TaskUpdateSchema,
    ):
        try:
            updated_task = TaskRepository.update_task(
                task=task, task_update_schema=task_update_schema
            )
            return response(
                {
                    "message": "Task updated successfully",
                    "task": updated_task.to_dict(
                        fields=[
                            "id",
                            "title",
                            "description",
                            "due_date",
                            "completed",
                        ]
                    ),
                },
                201,
            )
        except Exception as e:
            abort(400, message=str(e))

        for field, value in task_update_schema.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        db.session.commit()
        return task

    @staticmethod
    def delete_task(task_id: int):
        if TaskRepository.delete_task(task_id):
            return response(
                {"message": "Task deleted successfully"},
                200,
                {"Content-Type": "application/json"},
            )
        abort(500, message="Failed to delete task")
