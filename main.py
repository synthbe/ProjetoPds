from fastapi import FastAPI

from app.infrastructure import DatabaseInitializer
from app.config.middleware import MiddlewareManager
from app.router import Router
from app.config.swagger import SwaggerConfig
from ProjetoPds.app.infrastructure.techrepo.creator import MusicModelRepoCreator 

DatabaseInitializer.run()

app = FastAPI()

MiddlewareManager(app).setup()
Router(app).register()
app.openapi = SwaggerConfig().setup(app)

@app.on_event("startup")
async def startup_event():
    repo_manager = MusicModelRepoCreator.create()
    repo_manager.sync()                          
