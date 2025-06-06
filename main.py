from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.infrastructure import DatabaseInitializer
from app.config.middleware import MiddlewareManager
from app.router import Router
from app.config.swagger import SwaggerConfig
from app.infrastructure.techrepo.creator import MusicModelRepoCreator

DatabaseInitializer.run()
MusicModelRepoCreator.create()

app = FastAPI()

MiddlewareManager(app).setup()
Router(app).register()

app.openapi = SwaggerConfig().setup(app)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
