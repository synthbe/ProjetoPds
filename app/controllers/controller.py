from typing import Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass

from fastapi import APIRouter, Header, Depends

from app.dependencies import AuthGuard


@dataclass
class BaseController(ABC):
    def __init__(self, tags: list = []):
        self._router = APIRouter(tags=tags)
        self.add_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    @abstractmethod
    def add_routes(self) -> None: ...
