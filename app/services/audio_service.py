import shutil
from uuid import UUID
from pathlib import Path

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.repositories import AudioRepository
from app.models import Audio
from app.schemas.audio_schema import AudioCreate, AudioUpdate
from app.exceptions import NotFoundException


class AudioService:
    def __init__(self) -> None:
        self.audio_repository = AudioRepository()

    def get_by_id(self, id: int) -> Audio:
        audio = self.audio_repository.get_by_id(id)
        if not audio:
            raise NotFoundException("Audio not found")

        return audio

    def upload(self, file: UploadFile, user_id: UUID) -> Audio:
        save_path = Path(f"uploads/{file.filename}")
        save_path.parent.mkdir(parents=True, exist_ok=True)

        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        audio = self.audio_repository.create(
            AudioCreate(
                name=file.filename,  # pyright: ignore
                data_path=str(save_path),
                user_id=user_id,
            )
        )

        return audio

    def download(self, id: int, user_id: UUID):
        audio = self.get_by_id(id)

        if not audio or audio.user_id != user_id:
            raise NotFoundException("Audio not found.")

        file_path = Path(audio.data_path)

        if not file_path.exists():
            raise NotFoundException("Audio file not found on disk")

        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type="audio/mpeg",
        )

    def update(self, data: AudioUpdate, id: int) -> Audio:
        self.get_by_id(id)

        audio_updated = self.audio_repository.update(data, id)

        return audio_updated

    def delete(self, id: int) -> Audio:
        self.get_by_id(id)

        audio_deleted = self.audio_repository.delete(id)

        return audio_deleted
