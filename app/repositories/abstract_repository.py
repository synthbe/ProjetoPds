from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

T = TypeVar("T")
C = TypeVar("C")
U = TypeVar("U")

class AbstractRepository(ABC, Generic[T, C, U]):
    @abstractmethod
    def create(self, obj_data: C) -> T: pass

    @abstractmethod
    def get_by_id(self, obj_id: int) -> T | None: pass

    @abstractmethod
    def get_all(self,) -> List[T]: pass

    @abstractmethod
    def update(self, obj_data: U, obj_id: int) -> T | None: pass

    @abstractmethod
    def delete(self, obj_id: int) -> T | None: pass
