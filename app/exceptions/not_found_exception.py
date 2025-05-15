from .base_exception import AppBaseException


class NotFoundException(AppBaseException):

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=401)
