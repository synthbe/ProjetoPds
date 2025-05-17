from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
from app.infrastructure.singleton_meta import SingletonMeta


class DatabaseSessionManager(metaclass=SingletonMeta):
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL, echo=True)
        self.session_local = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session_local()

    def get_engine(self):
        return self.engine
