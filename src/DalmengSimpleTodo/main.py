from fastapi import FastAPI
import uvicorn

from DalmengSimpleTodo.routers.todo_router import todo_router
from DalmengSimpleTodo.database.database_repository import DatabaseRepository

from contextlib import asynccontextmanager

from fastapi.exceptions import RequestValidationError
from fastapi import Request
from DalmengSimpleTodo.models.base_model import BaseResponseModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    database_client = DatabaseRepository.get_client()
    await database_client.connect()
    yield
    await database_client.disconnect()
    
app = FastAPI(lifespan=lifespan)
app.include_router(todo_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> BaseResponseModel:
    error_details = exc.errors()
    error_messages = []

    for error in error_details:
        loc = ".".join([str(i) for i in error["loc"]])
        msg = f"{loc}: {error['msg']}"
        error_messages.append(msg)

    return BaseResponseModel.failed(
        status_code=422,
        msg="; ".join(error_messages)
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8181) # pragma: no cover