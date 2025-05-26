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
from app.infrastructure import ModelDownloader


class AudioService:
    def __init__(self) -> None:
        self.audio_repository = AudioRepository()
        self.audio_facade = AudioInference()
        self.model_downloader = ModelDownloader()
        self.allowed_types = [
            "audio/mpeg",
            "audio/wav",
            "audio/ogg",
            "audio/flac",
            "audio/aac",
        ]

    def find_by_id(self, id: UUID) -> Audio:
        audio = self.audio_repository.find_by_id(id)
        if not audio:
            raise NotFoundException("Audio not found")

        return audio

    def __save_audio(
        self,
        file: UploadFile,
        user_id: UUID,
    ) -> Audio:
        audio_id = uuid4()
        dir_path = Path(f"uploads/{user_id}/{audio_id}/")
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / file.filename
        
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

        return dir_path, audio

    def __apply_audio_extraction(
        self,
        dir_path: Path,
        user_id: UUID,
        extraction_type: Literal["vocals", "instrumental", "4stems"]
    ) -> List[Audio]:
        self.model_downloader.download_model(extraction_type)

        output_files = self.audio_facade.vocal_inference(str(dir_path), extraction_type)

        created_audios = []

        for output_file in output_files:
            new_audio = self.audio_repository.create(
                AudioCreate(
                id=uuid4(),
                name=output_file["name"],
                data_path=output_file["path"],
                user_id=user_id,
            ))
            
            created_audios.append(new_audio)

        return created_audios

    def upload(
        self,
        file: UploadFile,
        user_id: UUID,
        extraction_type: Literal["vocals", "instrumental", "4stems"]
    ) -> List[Audio]:
        if file.content_type not in self.allowed_types:
            allowed_types_str = ", ".join(self.allowed_types)
            raise AudioTypeNotSupportedException(
                f"Audio type not supported. Allowed types: {allowed_types_str}"
            )

        dir_path, audio = self.__save_audio(file, user_id)
        extracted_audios = self.__apply_audio_extraction(dir_path, user_id, extraction_type)
        
        extracted_audios.insert(0, audio) 
        
        return extracted_audios


    def download(self, id: UUID, user_id: UUID):
        audio = self.find_by_id(id)

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
        audio = self.find_by_id(id)

        audio_updated = self.audio_repository.update(data, audio)

        return audio_updated

    def delete(self, id: UUID) -> Audio:
        audio = self.find_by_id(id)

        audio_deleted = self.audio_repository.delete(audio)

        return audio_deleted
