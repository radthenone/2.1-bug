import logging
from typing import List, Optional

from app.database import db
from app.tasks.db import TaskModel
from app.tasks.schema import TaskCreateSchema, TaskUpdateSchema


class TaskRepository:
    @staticmethod
    def get_tasks_by_todo_id(todo_id: int) -> List["TaskModel"]:
        return TaskModel.query.filter_by(todo_id=todo_id).all()

    @staticmethod
    def get_task_by_todo_id(todo_id: int) -> "TaskModel":
        return TaskModel.query.filter_by(todo_id=todo_id).first()

    @staticmethod
    def get_task_by_id(task_id: int) -> "TaskModel":
        return TaskModel.query.filter_by(id=task_id).first()

    @staticmethod
    def exists_task(todo_id: int, title: str) -> bool:
        task = TaskModel.query.filter_by(todo_id=todo_id, title=title).first()
        if task:
            return True
        return False

    @staticmethod
    def create_task(task_schema: TaskCreateSchema, todo_id: int) -> "TaskModel":
        new_task = TaskModel(
            title=task_schema.title,
            description=task_schema.description,
            due_date=task_schema.due_date,
            todo_id=todo_id,
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task

    @staticmethod
    def update_task(
        task_update_schema: TaskUpdateSchema, task: "TaskModel"
    ) -> Optional["TaskModel"]:
        for field, value in task_update_schema.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        db.session.commit()
        return task

    @staticmethod
    def delete_task(task_id: int) -> bool:
        try:
            task = TaskRepository.get_task_by_id(task_id)
            db.session.delete(task)
            db.session.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False
