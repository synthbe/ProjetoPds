from models.audio_model import Audio
from schemas.audio_schema import AudioCreate, AudioUpdate
from repository import Repository

class AudioRepository(Repository[Audio, AudioCreate, AudioUpdate]):
    @property
    def model(self) -> type[Audio]:
        return Audio

    def toggle_audio_pin(self, id: int) -> Audio | None:
        audio = self.get_by_id(id)
        if not audio:
            return None
        audio.pinned = not audio.pinned

        return audio
