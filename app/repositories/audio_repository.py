from uuid import UUID
from sqlalchemy.orm import joinedload

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
        query = (
            self.db.query(Audio)
            .filter(Audio.user_id == user_id, Audio.parent_audio_id == None)
            .options(joinedload(Audio.children))
            .order_by(Audio.date_in.desc())
        )

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def is_parent(self, id: UUID) -> bool:
        audio = self.find_by_id(id)
        return audio.parent_audio_id is None
