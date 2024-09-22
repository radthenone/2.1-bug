from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TaskCreateSchema(BaseModel):
    title: str = Field(..., description="Title of the task", min_length=1)
    description: Optional[str] = Field(None, description="Optional task description")
    due_date: Optional[datetime] = Field(None, description="Optional due date")

    @field_validator("due_date", mode="before")
    def validate_due_date(cls, value):
        if isinstance(value, str):
            value = datetime.strptime(value, "%d:%m:%Y")
        if value and value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        if value and value < datetime.now(timezone.utc):
            raise ValueError("Due date cannot be in the past")
        return value


class TaskUpdateSchema(TaskCreateSchema):
    completed: Optional[bool] = Field(
        default=False, description="Task completion status"
    )


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    completed: bool
    todo_id: int
