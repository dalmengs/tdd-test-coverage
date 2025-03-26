from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List

from DalmengSimpleTodo.models.base_model import BaseResponseModel
from DalmengSimpleTodo.models.response.todo_response_model import TodoListResponseModel, TodoResponseModel
from DalmengSimpleTodo.models.request.todo_request_model import CreateTodoRequestModel, UpdateTodoRequestModel

from DalmengSimpleTodo.service.todo_service import TodoService
from DalmengSimpleTodo.exceptions.todo_exception import TodoNotFoundException, TodoAlreadyExistsException

todo_router = APIRouter(prefix="/api/v1/todo", tags=["todo"])

@todo_router.get("", response_model=BaseResponseModel[TodoListResponseModel])
async def api_get_todos():
    try:
        todos = await TodoService.get_todos()
        return BaseResponseModel.succeed(data=todos)
    except Exception as e:
        return BaseResponseModel.failed(msg=str(e))

@todo_router.post("", response_model=BaseResponseModel[TodoResponseModel])
async def create_todo(todo: CreateTodoRequestModel):
    try:
        todo = await TodoService.create_todo(todo)
        return BaseResponseModel.succeed(data=todo)
    except TodoAlreadyExistsException as e:
        return BaseResponseModel.failed(status_code=e.status_code, msg=e.msg)
    except Exception as e:
        return BaseResponseModel.failed(msg=str(e))

@todo_router.put("/{todo_id}", response_model=BaseResponseModel[TodoResponseModel])
async def update_todo(todo_id: str, todo: UpdateTodoRequestModel):
    try:
        todo = await TodoService.update_todo(todo_id, todo)
        return BaseResponseModel.succeed(data=todo)
    except TodoNotFoundException as e:
        return BaseResponseModel.failed(status_code=e.status_code, msg=e.msg)
    except Exception as e:
        return BaseResponseModel.failed(msg=str(e))

@todo_router.delete("/{todo_id}", response_model=BaseResponseModel[TodoResponseModel])
async def delete_todo(todo_id: str):
    try:
        todo = await TodoService.delete_todo(todo_id)
        return BaseResponseModel.succeed(data=todo)
    except TodoNotFoundException as e:
        return BaseResponseModel.failed(status_code=e.status_code, msg=e.msg)
    except Exception as e:
        return BaseResponseModel.failed(msg=str(e))