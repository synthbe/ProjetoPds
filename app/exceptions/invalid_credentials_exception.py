from .base_exception import AppBaseException


class InvalidCredentialsException(AppBaseException):

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, status_code=401)
