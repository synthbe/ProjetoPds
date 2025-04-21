from fastapi import FastAPI, Depends, APIRouter

from app.infrastructure import DatabaseInitializer
from app.config.middleware import MiddlewareManager
from app.router import Router
from app.dependencies.auth_guard import AuthGuard
from app.models.user_model import User


DatabaseInitializer.run()

app = FastAPI()

MiddlewareManager(app).setup()

Router(app).register()

router = APIRouter()


@router.get("/me")
def get_profile(current_user: User = Depends(AuthGuard.get_authenticated_user)):
    return {"email": current_user.email}


app.include_router(router)
