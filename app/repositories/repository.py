from abc import ABC
from app.infrastructure.database import DatabaseSessionManager


class Repository(ABC):
    def __init__(self):
        self.db = DatabaseSessionManager().get_session()
