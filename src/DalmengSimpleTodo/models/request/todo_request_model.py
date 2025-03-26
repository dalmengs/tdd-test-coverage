from pydantic import BaseModel
from typing import Optional

class BaseModelWrapper(BaseModel):
    def to_dict(self):
        return self.model_dump()

class CreateTodoRequestModel(BaseModelWrapper):
    title: str
    content: str

class UpdateTodoRequestModel(BaseModelWrapper):
    title: Optional[str] = None
    content: Optional[str] = None
