from .base_exception import AppBaseException


class ConflictException(AppBaseException):

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=404)
