import shutil
from uuid import UUID, uuid4
from pathlib import Path
from typing import Literal
from typing import List

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.repositories import AudioRepository
from app.models import Audio
from app.schemas.audio_schema import AudioCreate, AudioUpdate
from app.exceptions import NotFoundException, AudioTypeNotSupportedException
from app.facade import AudioInference


class AudioService:
    __ALLOWED_CONTENT_TYPES = [
        "audio/mpeg",
        "audio/wav",
        "audio/ogg",
        "audio/flac",
        "audio/aac",
    ]

    def __init__(self) -> None:
        self.audio_repository = AudioRepository()

    def get_by_id(self, id: int) -> Audio:
        audio = self.audio_repository.get_by_id(id)
        if not audio:
            raise NotFoundException("Audio not found")

        return audio

    def upload(self, file: UploadFile, user_id: UUID, extraction_type:Literal["vocal","4stems"]) -> List[Audio]:
        if file.content_type not in self.__ALLOWED_CONTENT_TYPES:
            allowed_types_str = ", ".join(self.__ALLOWED_CONTENT_TYPES)
            raise AudioTypeNotSupportedException(
                f"Audio type not supported. Allowed types: {allowed_types_str}"
            )

        audio_id = uuid4()
        dir_path = Path(f"uploads/{user_id}/{audio_id}/")
        dir_path.mkdir(parents=True, exist_ok=True)  # cria toda a estrutura necessária
        file_path = dir_path / file.filename         # melhor usar operador / para juntar paths

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        audio = self.audio_repository.create(
            AudioCreate(
                id=audio_id,
                name=file.filename,  # pyright: ignore
                data_path=str(file_path),
                user_id=user_id,
            )
        )

        created_audios = [audio]

        output_files = AudioInference.vocal_inference(str(dir_path),extraction_type)
        for file in output_files:
            audio_file = AudioCreate(
                id = uuid4(),
                name=file["name"],
                data_path=file["path"],
                user_id=user_id,
            )

            created_audios.append(self.audio_repository.create(audio_file))
        
        return created_audios


    def download(self, id: UUID, user_id: UUID):
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

    def update(self, data: AudioUpdate, id: UUID) -> Audio:
        self.get_by_id(id)

        audio_updated = self.audio_repository.update(data, id)

        return audio_updated

    def delete(self, id: UUID) -> Audio:
        self.get_by_id(id)

        audio_deleted = self.audio_repository.delete(id)

        return audio_deleted
