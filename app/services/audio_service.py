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

    def get_by_id(self, id: UUID) -> Audio:
        audio = self.audio_repository.get_by_id(id)
        if not audio:
            raise NotFoundException("Audio not found")
        return audio

    def upload(self, file: UploadFile, user_id: UUID, pipeline: List[str]) -> List[Audio]:
        if file.content_type not in self.__ALLOWED_CONTENT_TYPES:
            allowed_types_str = ", ".join(self.__ALLOWED_CONTENT_TYPES)
            raise AudioTypeNotSupportedException(
                f"Audio type not supported. Allowed types: {allowed_types_str}"
            )

        for model_key in pipeline:
            if model_key not in MODEL_CONFIG_MAP:
                raise ValueError(f"Unsupported model in pipeline: {model_key}")

        audio_id = uuid4()
        base_dir = Path(f"uploads/{user_id}/{audio_id}/")
        base_dir.mkdir(parents=True, exist_ok=True)
        original_file_path = base_dir / file.filename

        with original_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Save original audio to DB
        audio = self.audio_repository.create(
            AudioCreate(
                id=audio_id,
                name=file.filename,
                data_path=str(original_file_path),
                user_id=user_id,
            )
        )
        created_audios = [audio]

        current_input_path = base_dir

        for model_key in pipeline:
            output_files = AudioInference.pipeline_inference(str(current_input_path), model_key)

            created_this_step = []
            for file_info in output_files:
                audio_file = AudioCreate(
                    id=uuid4(),
                    name=file_info["name"],
                    data_path=file_info["path"],
                    user_id=user_id,
                )
                created_audio = self.audio_repository.create(audio_file)
                created_this_step.append(created_audio)

            created_audios.extend(created_this_step)

            if output_files:
                # Set input path for next model to the folder containing first output file
                first_output_path = Path(output_files[0]["path"]).parent
                current_input_path = first_output_path
            else:
                # No output, stop pipeline
                break

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
