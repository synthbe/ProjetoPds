
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.infrastructure.database import DatabaseSessionManager


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.db_manager = DatabaseSessionManager()

    async def dispatch(self, request: Request, call_next):
        session = self.db_manager.get_session()
        try:
            response = await call_next(request)
            session.commit()
            return response
        except Exception:
            session.rollback()
            raise
        finally:
            self.db_manager.remove_session()
