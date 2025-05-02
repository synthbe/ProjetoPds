from fastapi import Depends, File, UploadFile

from app.dependencies import AuthGuard
from app.services import AudioService
from app.schemas.audio_schema import AudioUpdate, AudioResponse
from app.models import User
from .controller import BaseController

class AudioController(BaseController):
    def __init__(self):
        super().__init__(tags=["Audio"], prefix="/audio")
        self.audio_service = AudioService()

    def add_routes(self) -> None:
        @self.router.post("/upload", response_model=AudioResponse)
        def upload(file: UploadFile = File(...), user: User = Depends(AuthGuard.get_authenticated_user)):
            audio = self.audio_service.upload(file, user.id)
            return AudioResponse.model_validate(audio)

        @self.router.get("/download/{id}")
        def download(id: int, user: User = Depends(AuthGuard.get_authenticated_user)):
            return self.audio_service.download(id, user.id)

        @self.router.put("/update/{id}")
        def update(id: int, data: AudioUpdate, user: User = Depends(AuthGuard.get_authenticated_user)):
            audio_updated = self.audio_service.update(data, id)
            return AudioResponse.model_validate(audio_updated)

        @self.router.delete("/delete/{id}", status_code=204)
        def delete(id: int, user: User = Depends(AuthGuard.get_authenticated_user)):
            audio_deleted = self.audio_service.delete(id)
            return AudioResponse.model_validate(audio_deleted)
