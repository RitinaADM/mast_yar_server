class ServerError(Exception):
    pass

class InvalidPaginationError(ServerError):
    pass

class DatabaseError(ServerError):
    pass