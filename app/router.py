from fastapi import FastAPI

from app.controllers import AuthController, UserController


class Router:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    def register(self):
        controller_classes = [AuthController, UserController]

        for controller_class in controller_classes:
            controller = controller_class()
            self.app.include_router(controller.router)
