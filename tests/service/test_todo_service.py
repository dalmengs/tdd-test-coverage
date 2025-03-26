from DalmengSimpleTodo.service.todo_service import TodoService
from DalmengSimpleTodo.models.request.todo_request_model import CreateTodoRequestModel

from unittest.mock import AsyncMock, patch
import pytest

class TestTodoService:
    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.DatabaseRepository.get_client")
    async def test_get_todos(self, mock_get_client):
        mock_prisma = AsyncMock()
        mock_get_client.return_value = mock_prisma
        mock_prisma.todo.find_many.return_value = [
            {"id": "123", "title": "Test Title", "content": "Test Content"}
        ]

        result = await TodoService.get_todos()
        assert result == [
            {"id": "123", "title": "Test Title", "content": "Test Content"}
        ]
    
    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.DatabaseRepository.get_client")
    async def test_get_todo_by_id(self, mock_get_client):
        mock_prisma = AsyncMock()
        mock_get_client.return_value = mock_prisma  
        mock_prisma.todo.find_unique.return_value = {
            "id": "123",
            "title": "Test Title",
            "content": "Test Content"
        }

        result = await TodoService._get_todo_by_id("123")
        assert result == {
            "id": "123",
            "title": "Test Title",
            "content": "Test Content"
        }

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.DatabaseRepository.get_client")
    async def test_get_todo_by_id_failed_with_todo_not_found(self, mock_get_client):
        mock_prisma = AsyncMock()
        mock_get_client.return_value = mock_prisma
        mock_prisma.todo.find_unique.return_value = None

        from DalmengSimpleTodo.exceptions.todo_exception import TodoNotFoundException
        with pytest.raises(TodoNotFoundException):
            await TodoService._get_todo_by_id("123")
        
    
    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.DatabaseRepository.get_client")
    async def test_create_todo(self, mock_get_client):
        # Arrange
        mock_prisma = AsyncMock()
        mock_get_client.return_value = mock_prisma
        mock_prisma.todo.create.return_value = {
            "id": "123",
            "title": "Test Title",
            "content": "Test Content"
        }

        request = CreateTodoRequestModel(title="Test Title", content="Test Content")

        # Act
        result = await TodoService.create_todo(request)

        # Assert
        mock_prisma.todo.create.assert_awaited_once_with(data=request.to_dict())
        assert result["title"] == "Test Title"

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.DatabaseRepository.get_client")
    async def test_update_todo(self, mock_get_client):
        mock_prisma = AsyncMock()
        mock_get_client.return_value = mock_prisma
        mock_prisma.todo.update.return_value = {
            "id": "123",
            "title": "Updated Title",
            "content": "Updated Content"
        }

        from DalmengSimpleTodo.models.request.todo_request_model import UpdateTodoRequestModel
        request = UpdateTodoRequestModel(title="Updated Title", content="Updated Content")

        result = await TodoService.update_todo("123", request)

        mock_prisma.todo.update.assert_awaited_once_with(where={"id": "123"}, data=request.to_dict())
        assert result["title"] == "Updated Title"

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.DatabaseRepository.get_client")
    async def test_delete_todo(self, mock_get_client):
        mock_prisma = AsyncMock()
        mock_get_client.return_value = mock_prisma
        mock_prisma.todo.delete.return_value = {
            "id": "123",
            "title": "Test Title",
            "content": "Test Content"
        }

        result = await TodoService.delete_todo("123")

        mock_prisma.todo.delete.assert_awaited_once_with(where={"id": "123"})
        assert result["title"] == "Test Title"
    
    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService._get_todo_by_id")
    async def test_delete_todo_failed_with_todo_not_found(self, mock_get_todo_by_id):
        from DalmengSimpleTodo.exceptions.todo_exception import TodoNotFoundException
        mock_get_todo_by_id.side_effect = TodoNotFoundException("Todo not found")

        with pytest.raises(TodoNotFoundException):
            await TodoService.delete_todo("123")
