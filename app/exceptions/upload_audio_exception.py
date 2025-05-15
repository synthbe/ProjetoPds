from .base_exception import AppBaseException


class AudioTypeNotSupportedException(AppBaseException):

    def __init__(self, message: str = "Audio type not supported") -> None:
        super().__init__(message, status_code=415)
