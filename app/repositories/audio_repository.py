from sqlalchemy.orm import Session
from typing import List

from models.audio_model import Audio
from schemas.audio_schema import AudioCreate, AudioUpdate
from abstract_repository import AbstractRepository

class AudioRepository(AbstractRepository[Audio, AudioCreate, AudioUpdate]):
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_data: AudioCreate) -> Audio:
        audio = Audio(
            name=obj_data.name,
            pinned=False,
        )
        self.db.add(audio)
        self.db.commit()
        self.db.refresh(audio)
        return audio

    def get_by_id(self, obj_id: int) -> Audio | None:
        return self.db.query(Audio).filter(Audio.id == obj_id).first()

    def get_all(self) -> List[Audio]:
        return self.db.query(Audio).all()

    def update(self, obj_data: AudioUpdate, obj_id: int) -> Audio | None:
        audio = self.get_by_id(obj_id)
        if not audio:
            return None

        if obj_data.name is not None:
            audio.name = obj_data.name

        self.db.commit()
        self.db.refresh(audio)

        return audio

    def delete(self, obj_id: int) -> Audio | None:
        audio = self.get_by_id(obj_id)
        if not audio:
            return None

        self.db.delete(audio)
        self.db.commit()

        return audio

    def toggle_audio_pin(self, obj_id: int) -> Audio | None:
        audio = self.get_by_id(obj_id)
        if not audio:
            return None
        audio.pinned = not audio.pinned

        return audio
