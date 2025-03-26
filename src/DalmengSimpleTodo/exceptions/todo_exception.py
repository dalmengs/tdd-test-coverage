class TodoNotFoundException(Exception):
    status_code = 404
    msg = "Todo not found"

class TodoAlreadyExistsException(Exception):
    status_code = 400
    msg = "Todo already exists. Use a different title."
