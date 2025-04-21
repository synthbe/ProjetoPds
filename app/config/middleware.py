from fastapi import FastAPI
from app.middlewares.exception_handler import ExceptionHandlerMiddleware


class MiddlewareManager:
    def __init__(self, app: FastAPI):
        self.app = app

    def setup(self):
        self._add_exception_handler()

    def _add_exception_handler(self):
        self.app.add_middleware(ExceptionHandlerMiddleware)
