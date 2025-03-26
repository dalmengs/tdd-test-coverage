from pydantic import BaseModel
from typing import List

class TodoResponseModel(BaseModel):
    id: int
    title: str
    content: str

class TodoListResponseModel(BaseModel):
    todos: List[TodoResponseModel]
