import pytest
from unittest.mock import patch

class TestTodo:
    # ==============================================================
    # [GET] /api/v1/todo
    # ==============================================================

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.get_todos")
    async def test_get_todos_success(self, mock_get_todos, test_client):
        mock_get_todos.return_value = [
            {
                "id": "67e42cbd23fd49969709329a",
                "title": "Test",
                "content": "Mocked content"
            }
        ]

        response = await test_client.get("/api/v1/todo")
        response = response.json()

        assert response["status_code"] == 200
        assert response["data"] == mock_get_todos.return_value

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.get_todos")
    async def test_get_todos_failed_with_prisma_error(self, mock_get_todos, test_client):
        mock_get_todos.side_effect = Exception("Prisma Error")

        response = await test_client.get("/api/v1/todo")
        response = response.json()

        assert response["status_code"] == 500

    # ==============================================================
    # [POST] /api/v1/todo
    # ==============================================================

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.create_todo")
    async def test_create_todo_success(self, mock_create_todo, test_client):
        request_title = "Test"
        request_content = "Mocked content"  

        mock_create_todo.return_value = {
            "id": "67e42cbd23fd49969709329a",
            "title": request_title,
            "content": request_content
        }
        
        response = await test_client.post("/api/v1/todo", json={"title": request_title, "content": request_content})
        response = response.json()

        assert response["status_code"] == 200
        assert response["data"]["id"] == "67e42cbd23fd49969709329a"
        assert response["data"]["title"] == request_title
        assert response["data"]["content"] == request_content

    @pytest.mark.asyncio
    async def test_create_todo_failed_with_missing_title(self, test_client):
        response = await test_client.post("/api/v1/todo", json={"content": "Mocked content"})
        response = response.json()

        assert response["status_code"] == 422

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.create_todo")
    async def test_create_todo_failed_with_prisma_error(self, mock_create_todo, test_client):
        mock_create_todo.side_effect = Exception("Prisma Error")

        response = await test_client.post("/api/v1/todo", json={"title": "Test Title", "content": "Mocked content"})
        response = response.json()

        assert response["status_code"] == 500

    
    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.create_todo")
    async def test_create_todo_failed_with_todo_already_exists(self, mock_create_todo, test_client):
        from DalmengSimpleTodo.exceptions.todo_exception import TodoAlreadyExistsException
        mock_create_todo.side_effect = TodoAlreadyExistsException("Todo already exists")

        response = await test_client.post("/api/v1/todo", json={"title": "Test Title", "content": "Mocked content"})
        response = response.json()

        assert response["status_code"] == 400

    # ==============================================================
    # [PUT] /api/v1/todo/{todo_id}
    # ==============================================================

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.update_todo")
    async def test_update_todo_failed_with_missing_title_and_content(self, mock_update_todo, test_client):
        mock_update_todo.return_value = {
            "id": "67e42cbd23fd49969709329a",
            "title": "Updated Title",
            "content": "Updated Content"
        }

        response = await test_client.put("/api/v1/todo/67e42cbd23fd49969709329a", json={})
        response = response.json()

        assert response["status_code"] == 200
        assert response["data"]["id"] == "67e42cbd23fd49969709329a"
        assert response["data"]["title"] == "Updated Title"
        assert response["data"]["content"] == "Updated Content"

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.update_todo")
    async def test_update_todo_success(self, mock_update_todo, test_client):
        mock_update_todo.return_value = {
            "id": "67e42cbd23fd49969709329a",
            "title": "Updated Title",
            "content": "Updated Content"
        }

        response = await test_client.put("/api/v1/todo/67e42cbd23fd49969709329a", json={"title": "Updated Title", "content": "Updated Content"})
        response = response.json()

        assert response["status_code"] == 200
        assert response["data"]["id"] == "67e42cbd23fd49969709329a"
        assert response["data"]["title"] == "Updated Title"
        assert response["data"]["content"] == "Updated Content"
    
    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.update_todo")
    async def test_update_todo_succeed_with_missing_title(self, mock_update_todo, test_client):
        mock_update_todo.return_value = {
            "id": "67e42cbd23fd49969709329a",
            "title": "Updated Title",
            "content": "Updated Content"
        }

        response = await test_client.put("/api/v1/todo/67e42cbd23fd49969709329a", json={"content": "Updated Content"})
        response = response.json()

        assert response["status_code"] == 200
        assert response["data"]["id"] == "67e42cbd23fd49969709329a"
        assert response["data"]["title"] == "Updated Title"
        assert response["data"]["content"] == "Updated Content"

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.update_todo")
    async def test_update_todo_succeed_with_missing_title_and_content(self, mock_update_todo, test_client):
        mock_update_todo.return_value = {
            "id": "67e42cbd23fd49969709329a",
            "title": "Title",
            "content": "Content"
        }

        response = await test_client.put("/api/v1/todo/67e42cbd23fd49969709329a", json={})
        response = response.json()

        assert response["status_code"] == 200
        assert response["data"]["id"] == "67e42cbd23fd49969709329a"
        assert response["data"]["title"] == "Title"
        assert response["data"]["content"] == "Content"

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.update_todo")
    async def test_update_todo_failed_with_prisma_error(self, mock_update_todo, test_client):
        mock_update_todo.side_effect = Exception("Prisma Error")

        response = await test_client.put("/api/v1/todo/67e42cbd23fd49969709329a", json={"title": "Updated Title", "content": "Updated Content"})
        response = response.json()

        assert response["status_code"] == 500
    
    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.update_todo")
    async def test_update_todo_failed_with_todo_not_found(self, mock_update_todo, test_client):
        from DalmengSimpleTodo.exceptions.todo_exception import TodoNotFoundException
        mock_update_todo.side_effect = TodoNotFoundException("Todo not found")

        response = await test_client.put("/api/v1/todo/67e42cbd23fd49969709329a", json={"title": "Updated Title", "content": "Updated Content"})
        response = response.json()  

        assert response["status_code"] == 404

    # ==============================================================
    # [DELETE] /api/v1/todo/{todo_id}
    # ==============================================================

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.delete_todo")
    async def test_delete_todo_success(self, mock_delete_todo, test_client):
        mock_delete_todo.return_value = {
            "id": "67e42cbd23fd49969709329a",
            "title": "Title",
            "content": "Content"
        }

        response = await test_client.delete("/api/v1/todo/67e42cbd23fd49969709329a")
        response = response.json()

        assert response["status_code"] == 200
        assert response["data"]["id"] == "67e42cbd23fd49969709329a"
        assert response["data"]["title"] == "Title"
        assert response["data"]["content"] == "Content"
    
    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.delete_todo")
    async def test_delete_todo_failed(self, mock_delete_todo, test_client):
        from DalmengSimpleTodo.exceptions.todo_exception import TodoNotFoundException
        mock_delete_todo.side_effect = TodoNotFoundException("Todo not found")

        response = await test_client.delete("/api/v1/todo/67e42cbd23fd49969709329a")
        response = response.json()

        assert response["status_code"] == 404

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.delete_todo")
    async def test_delete_todo_failed_with_missing_id(self, mock_delete_todo, test_client):
        from DalmengSimpleTodo.exceptions.todo_exception import TodoNotFoundException
        mock_delete_todo.side_effect = Exception("Invalid object id parsing")

        response = await test_client.delete("/api/v1/todo/adf")
        response = response.json()

        assert response["status_code"] == 500

    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.delete_todo")
    async def test_delete_todo_failed_with_not_found(self, mock_delete_todo, test_client):
        from DalmengSimpleTodo.exceptions.todo_exception import TodoNotFoundException
        mock_delete_todo.side_effect = TodoNotFoundException("Todo not found")

        response = await test_client.delete("/api/v1/todo/67e42cbd23fd49969709329a")
        response = response.json()

        assert response["status_code"] == 404
    
    @pytest.mark.asyncio
    @patch("DalmengSimpleTodo.service.todo_service.TodoService.delete_todo")
    async def test_delete_todo_succeed(self, mock_delete_todo, test_client):
        mock_delete_todo.return_value = {
            "id": "67e42cbd23fd49969709329a",
            "title": "Title",
            "content": "Content"
        }

        response = await test_client.delete("/api/v1/todo/67e42cbd23fd49969709329a")
        response = response.json()

        assert response["status_code"] == 200
        assert response["data"]["id"] == "67e42cbd23fd49969709329a"
        assert response["data"]["title"] == "Title"
        assert response["data"]["content"] == "Content"
