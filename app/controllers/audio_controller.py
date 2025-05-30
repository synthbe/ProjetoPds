from uuid import UUID
from fastapi import Depends, File, UploadFile, Form
from typing import List
from app.dependencies import AuthGuard
from app.services import AudioService
from app.schemas.audio_schema import (
    AudioUpdate,
    AudioSingleResponse,
    AudioParentResponse,
)
from app.models import User
from .controller import BaseController


class AudioController(BaseController):
    def __init__(self):
        super().__init__(tags=["Audio"], prefix="/audio")
        self.audio_service = AudioService()

    def add_routes(self) -> None:
        @self.router.get("/", response_model=List[AudioParentResponse])
        def get_all(user: User = Depends(AuthGuard.get_authenticated_user)):
            audios = self.audio_service.get_all(user.id)
            return [AudioParentResponse.model_validate(audio) for audio in audios]

        @self.router.post("/upload", response_model=List[AudioSingleResponse])
        def upload(
            file: UploadFile = File(...),
            user: User = Depends(AuthGuard.get_authenticated_user),
            pipeline: str = Form(...),
        ):
            pipeline_list = [p.strip() for p in pipeline.split(",") if p.strip()]
            audio = self.audio_service.upload(file, user.id, pipeline_list)
            return [
                AudioSingleResponse.model_validate(children)
                for children in audio.children
            ]

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
            return AudioSingleResponse.model_validate(audio_updated)

        @self.router.delete("/delete/{id}", status_code=204)
        def delete(id: UUID, _: User = Depends(AuthGuard.get_authenticated_user)):
            audio_deleted = self.audio_service.delete(id)
            return AudioSingleResponse.model_validate(audio_deleted)
