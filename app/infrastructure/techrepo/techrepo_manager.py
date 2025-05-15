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
        print(f"⏬ Clonando repo de {self.repo_url} pra pasta '{self.clone_dir}'...")
        git.Repo.clone_from(self.repo_url, self.clone_dir)
        print("✅ Clonagem feita")

    def _update_repo(self):
        print("🔄 Repo já existe, tentando puxar atualizações...")
        try:
            repo = git.Repo(self.clone_dir)
            origin = repo.remotes.origin
            origin.fetch()
            origin.pull()
            print("✅ Repo atualizado")
        except GitCommandError as e:
            print(f"⚠️ Erro ao atualizar o repo: {e}")
            print("🔁 Fazendo reset total pro que tá no remoto...")
            repo.git.reset('--hard')
            origin.pull()
            print("✅ Reset feito e repo atualizado")

    def _install_requirements(self):
        print("🔧 Instalando dependências do requirements.txt do repo...")
        requirements_path = os.path.join(self.clone_dir, "requirements.txt")
        subprocess.run(["uv", "pip", "install", "-r", requirements_path], check=True)
        print("✅ Dependências instaladas")
