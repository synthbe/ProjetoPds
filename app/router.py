from fastapi import FastAPI

from app.controllers import AuthController


class Router:
    def __init__(self, app: FastAPI):
        self.app = app

    def register(self):
        controller_classes = [AuthController]

        for controller_class in controller_classes:
            controller = controller_class()
            self.app.include_router(controller.router)
