from fastapi import APIRouter
from typing import Protocol


class IController(Protocol):
    @property
    def router(self) -> APIRouter: ...

    def add_routes(self) -> None: ...
