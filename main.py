from fastapi import FastAPI

from app.infrastructure import DatabaseInitializer
from app.config.middleware import MiddlewareManager
from app.router import Router
from app.config.swagger import SwaggerConfig
from app.infrastructure.update_techrepo import sync_music_model_repo

DatabaseInitializer.run()

app = FastAPI()

MiddlewareManager(app).setup()

Router(app).register()

app.openapi = SwaggerConfig().setup(app)

@app.on_event("startup")
async def startup_event():
    sync_music_model_repo()
