from app.config.settings import settings
from app.infrastructure.techrepo.techrepo_manager import MusicModelRepoManager


class MusicModelRepoCreator:
    @staticmethod
    def create() -> MusicModelRepoManager:
        music_model_repo_manager = MusicModelRepoManager(
            repo_url=settings.AUDIO_EXTRACTOR_REPO_URL,
            clone_dir=settings.AUDIO_EXTRACTOR_REPO_DIR,
        )

        music_model_repo_manager.sync()
