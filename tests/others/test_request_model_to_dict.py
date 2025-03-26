from DalmengSimpleTodo.models.request.todo_request_model import CreateTodoRequestModel

def test_create_todo_request_model_to_dict():
    test_model = CreateTodoRequestModel(title="Test Title", content="Test Content")
    expected = {"title": "Test Title", "content": "Test Content"}

    result = test_model.to_dict()

    assert result == expected
