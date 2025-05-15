from app.config.settings import settings
from app.infrastructure.techrepo.techrepo_manager import MusicModelRepoManager


class MusicModelRepoCreator:
    @staticmethod
    def create() -> MusicModelRepoManager:
        return MusicModelRepoManager(
            repo_url=settings.REPO_URL,
            clone_dir=settings.CLONE_DIR
        )
