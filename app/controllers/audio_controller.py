from uuid import UUID

from fastapi import Depends, File, UploadFile, Form

from app.dependencies import AuthGuard
from app.services import AudioService
from app.schemas.audio_schema import AudioUpdate, AudioResponse
from app.models import User
from typing import Literal

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
            extraction_type: Literal["vocal","4stems"] = Form(...)
        ):
            audio = self.audio_service.upload(file, user.id, extraction_type)
            return AudioResponse.model_validate(audio)

        @self.router.get("/download/{id}")
        def download(id: UUID, user: User = Depends(AuthGuard.get_authenticated_user)):
            return self.audio_service.download(id, user.id)

        @self.router.put("/update/{id}")
        def update(
            id: UUID,
            data: AudioUpdate,
            _: User = Depends(AuthGuard.get_authenticated_user),
        ):
            audio_updated = self.audio_service.update(data, id)
            return AudioResponse.model_validate(audio_updated)

        @self.router.delete("/delete/{id}", status_code=204)
        def delete(id: UUID, _: User = Depends(AuthGuard.get_authenticated_user)):
            audio_deleted = self.audio_service.delete(id)
            return AudioResponse.model_validate(audio_deleted)
