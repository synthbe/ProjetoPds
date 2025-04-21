from .base_exception import AppBaseException


class NotFoundException(AppBaseException):

    def __init__(self, message: str):
        super().__init__(message, status_code=401)
