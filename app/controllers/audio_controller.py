from fastapi import Depends, File, HTTPException, UploadFile

from app.dependencies import AuthGuard
from app.exceptions.not_found_exception import NotFoundException
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
        def upload(
            file: UploadFile = File(...),
            user: User = Depends(AuthGuard.get_authenticated_user),
        ):
            try:
                audio = self.audio_service.upload(file, user.id)
                return AudioResponse.model_validate(audio)
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.get("/download/{id}")
        def download(id: int, user: User = Depends(AuthGuard.get_authenticated_user)):
            try:
                return self.audio_service.download(id, user.id)
            except Exception as e:
                raise HTTPException(status_code=404, detail=str(e))

        @self.router.put("/update/{id}")
        def update(
            id: int,
            data: AudioUpdate,
            user: User = Depends(AuthGuard.get_authenticated_user),
        ):
            try:
                audio_updated = self.audio_service.update(data, id)
                return AudioResponse.model_validate(audio_updated)
            except NotFoundException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)

        @self.router.delete("/delete/{id}", status_code=204)
        def delete(id: int, user: User = Depends(AuthGuard.get_authenticated_user)):
            try:
                audio_deleted = self.audio_service.delete(id)
                return AudioResponse.model_validate(audio_deleted)
            except NotFoundException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)
