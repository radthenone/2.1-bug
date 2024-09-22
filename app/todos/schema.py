from pydantic import BaseModel


class TodoCreateSchema(BaseModel):
    name: str
    user_id: int


class TodoUpdateSchema(BaseModel):
    name: str


class TodoResponse(BaseModel):
    id: int
    name: str
    user_id: int
