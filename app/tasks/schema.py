from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, FutureDate, StringConstraints


class TodoCreateSchema(BaseModel):
    title = Annotated[str, StringConstraints(min_length=5)]
    description = Annotated[Optional[str], StringConstraints(min_length=10)]
    due_date = Annotated[Optional[datetime], FutureDate()]


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    completed: bool
    todo_id: int
