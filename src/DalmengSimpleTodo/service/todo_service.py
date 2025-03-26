from DalmengSimpleTodo.database.database_repository import DatabaseRepository
from DalmengSimpleTodo.models.request.todo_request_model import CreateTodoRequestModel, UpdateTodoRequestModel
from DalmengSimpleTodo.exceptions.todo_exception import TodoNotFoundException

class TodoService:
    @staticmethod
    async def get_todos():
        todos = await DatabaseRepository.get_client().todo.find_many()
        return todos
    
    @staticmethod
    async def create_todo(todo: CreateTodoRequestModel):
        return await DatabaseRepository.get_client().todo.create(data=todo.to_dict())
    
    @staticmethod
    async def update_todo(todo_id: str, todo: UpdateTodoRequestModel):
        await TodoService._get_todo_by_id(todo_id)
        return await DatabaseRepository.get_client().todo.update(where={"id": todo_id}, data=todo.to_dict())
    
    @staticmethod
    async def delete_todo(todo_id: str):
        await TodoService._get_todo_by_id(todo_id)
        return await DatabaseRepository.get_client().todo.delete(where={"id": todo_id})
    
    @staticmethod
    async def _get_todo_by_id(todo_id: str):
        todo = await DatabaseRepository.get_client().todo.find_unique(where={"id": todo_id})
        if not todo:
            raise TodoNotFoundException(f"Todo with id {todo_id} not found")
        return todo
    