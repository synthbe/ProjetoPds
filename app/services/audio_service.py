import shutil
from uuid import UUID, uuid4
from pathlib import Path
from typing import List

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.repositories import AudioRepository
from app.models import Audio
from app.schemas.audio_schema import AudioCreate, AudioUpdate
from app.exceptions import NotFoundException, AudioTypeNotSupportedException
from app.facade.audio_inference_facade import AudioInference, MODEL_CONFIG_MAP
from app.infrastructure import ModelDownloader

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

    def upload(self, file: UploadFile, user_id: UUID, pipeline: List[str]) -> Audio:
        self._validate_upload(file, pipeline)

        audio_id = uuid4()
        base_dir = Path(f"uploads/{user_id}/{audio_id}/")
        base_dir.mkdir(parents=True, exist_ok=True)
        original_file_path = base_dir / file.filename # pyright: ignore

        with original_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Save original audio to DB
        original_audio = self._create_audio_instance(
            audio_id, file.filename, str(original_file_path), user_id # pyright: ignore
        )

        current_input_path = base_dir
        for model_key in pipeline:
            current_input_path= self._run_pipeline_step(
                model_key, current_input_path, user_id, original_audio.id
            )

        return original_audio

    def _validate_upload(self, file: UploadFile, pipeline: List[str]) -> None:
        if file.content_type not in self.__ALLOWED_CONTENT_TYPES:
            allowed = ", ".join(self.__ALLOWED_CONTENT_TYPES)
            raise AudioTypeNotSupportedException(f"Audio type not supported. Allowed: {allowed}")
        for key in pipeline:
            if key not in MODEL_CONFIG_MAP:
                raise ValueError(f"Unsupported model in pipeline: {key}")

    def _create_audio_instance(self, audio_id: UUID, name: str, path: str, user_id: UUID, parent_id: UUID | None = None) -> Audio:
        return self.audio_repository.create(
            AudioCreate(
                id=audio_id,
                name=name,
                data_path=path,
                user_id=user_id,
                parent_audio_id=parent_id
            )
        )

    def _run_pipeline_step(self, model_key: str, input_path: Path, user_id: UUID, parent_id: UUID) -> Path:
        self.model_downloader.download_model(model_key)
        outputs = self.audio_facade.pipeline_inference(str(input_path), model_key)
        audios = []
        for output in outputs:
            audio = self._create_audio_instance(
                uuid4(), output["name"], output["path"], user_id, parent_id
            )
            audios.append(audio)

        next_input = Path(outputs[0]["path"]).parent if outputs else input_path
        return next_input
