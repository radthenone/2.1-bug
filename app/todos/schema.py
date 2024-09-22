from typing import Annotated

from pydantic import BaseModel


class TodoCreateSchema(BaseModel):
    name: str
    user_id: int


class TodoResponse(BaseModel):
    id: int
    name: str
    user_id: int
