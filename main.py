from fastapi import FastAPI

from app.infrastructure import DatabaseInitializer
from app.config.middleware import MiddlewareManager
from app.config.swagger import SwaggerConfig
from app.router import Router


DatabaseInitializer.run()

app = FastAPI()

MiddlewareManager(app).setup()

Router(app).register()

app.openapi = SwaggerConfig(app)
