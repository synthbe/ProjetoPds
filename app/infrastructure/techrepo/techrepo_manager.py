import os
import subprocess
import git

from git.exc import GitCommandError


class MusicModelRepoManager:
    def __init__(self, repo_url: str, clone_dir: str):
        self.repo_url = repo_url
        self.clone_dir = clone_dir

    def sync(self):
        if not os.path.exists(self.clone_dir):
            self._clone_repo()
        else:
            self._update_repo()

        self._install_requirements()

    def _clone_repo(self):
        print(f"⏬ Cloning repo from {self.repo_url} into folder '{self.clone_dir}'...")
        git.Repo.clone_from(self.repo_url, self.clone_dir)
        print("✅ Clone completed")

    def _update_repo(self):
        print("🔄 Repo already exists, trying to pull updates...")
        try:
            repo = git.Repo(self.clone_dir)
            origin = repo.remotes.origin
            origin.fetch()
            origin.pull()
            print("✅ Repo updated")
        except GitCommandError as e:
            print(f"⚠️ Error while updating repo: {e}")
            print("🔁 Performing hard reset to match remote...")
            repo.git.reset("--hard")
            origin.pull()
            print("✅ Reset completed and repo updated")

    def _install_requirements(self):
        print("🔧 Installing dependencies from repo's requirements.txt...")
        requirements_path = os.path.join(self.clone_dir, "requirements.txt")
        subprocess.run(["uv", "pip", "install", "-r", requirements_path], check=True)
        print("✅ Dependencies installed")
