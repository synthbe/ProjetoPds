from app.infrastructure import DatabaseInitializer
from fastapi import FastAPI
from app.config.middleware import MiddlewareManager

DatabaseInitializer.run()

app = FastAPI()

MiddlewareManager(app).setup()


@app.get("/")
def root():
    return {"Hello": "World"}
