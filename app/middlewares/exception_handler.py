from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi.responses import JSONResponse
from fastapi import Request
from app.exceptions import AppBaseException
from app.config import Logger


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            response = await call_next(request)
            return response
        except AppBaseException as e:
            error_response = {
                "message": e.message,
            }

            if e.errors:
                error_response["errors"] = e.errors

            return JSONResponse(
                status_code=e.status_code,
                content=error_response,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            Logger.error(f"{request.method} {request.url.path}", str(e))
            return JSONResponse(
                status_code=500, content={"message": "Internal Server Error"}
            )
