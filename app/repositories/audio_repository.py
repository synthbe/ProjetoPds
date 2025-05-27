from uuid import UUID

from app.models.audio_model import Audio
from app.schemas.audio_schema import AudioCreate, AudioUpdate

from .repository import Repository


class AudioRepository(Repository[Audio, AudioCreate, AudioUpdate]):
    @property
    def model(self) -> type[Audio]:
        return Audio

    def find_audios_by_user_id(
        self, user_id: UUID, limit: int | None = None
    ) -> list[Audio]:
        return (
            self.db.query(Audio)
            .filter(Audio.user_id == user_id)
            .order_by(Audio.date_in.desc())
            .limit(limit)
            .all()
        )

    def is_parent(self, id: UUID) -> bool:
        audio = self.find_by_id(id)
        return audio.parent_audio_id is None
