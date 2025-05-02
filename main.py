from fastapi import FastAPI
from app.infrastructure.update_techrepo import sync_music_model_repo

from app.infrastructure import DatabaseInitializer

DatabaseInitializer.run()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    sync_music_model_repo()

@app.get("/")
def root():
    return {"oi": "gagui"}
