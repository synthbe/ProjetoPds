from app.infrastructure import DatabaseInitializer
from fastapi import FastAPI

DatabaseInitializer.run()
app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}
