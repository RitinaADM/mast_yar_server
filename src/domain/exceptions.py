class ServerError(Exception):
    """Базовое исключение для ошибок сервера."""
    pass

class InvalidPaginationError(ServerError):
    """Исключение, возникающее при недопустимых параметрах пагинации."""
    pass

class DatabaseError(ServerError):
    """Исключение, возникающее при ошибках базы данных."""
    pass