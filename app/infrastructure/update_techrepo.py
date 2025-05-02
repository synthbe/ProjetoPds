import os
import subprocess
import git
from git.exc import GitCommandError
from app.config.settings import settings


def sync_music_model_repo():
    if not os.path.exists(settings.AUDIO_EXTRACTOR_REPO_DIR):
        print(
            f"⏬ clonando repo de {settings.AUDIO_EXTRACTOR_REPO_URL} pra pasta '{settings.AUDIO_EXTRACTOR_REPO_DIR}'..."
        )
        git.Repo.clone_from(
            settings.AUDIO_EXTRACTOR_REPO_URL, settings.AUDIO_EXTRACTOR_REPO_DIR
        )
        print("✅ clonagem feita")

        # instala as dependências que tão no requirements.txt
        print("🔧 instalando dependências do requirements.txt do repo...")
        subprocess.run(
            [
                "uv",
                "pip",
                "install",
                "-r",
                os.path.join(settings.AUDIO_EXTRACTOR_REPO_DIR, "requirements.txt"),
            ]
        )
        print("✅ dependências instaladas")
    else:
        print("🔄 repo já existe, tentando puxar atualizações...")

        try:
            repo = git.Repo(settings.AUDIO_EXTRACTOR_REPO_DIR)
            origin = repo.remotes.origin
            origin.fetch()  # pega os commits novos do remoto
            origin.pull()  # puxa as mudanças pro diretório atual
            print("✅ repo atualizado")
        except GitCommandError as e:
            print(f"⚠️ deu erro ao tentar atualizar o repo: {e}")
            print("fazendo reset total pro que tá no remoto...")
            repo.git.reset("--hard")  # reseta tudo pras últimas alterações do remoto
            origin.pull()  # puxa dnv depois do reset
            print("✅ reset feito e repo atualizado")

    # sempre instala as dependências dps de clonar ou atualizar
    print("🔧 instalando dependências do requirements.txt do repo...")
    subprocess.run(
        [
            "uv",
            "pip",
            "install",
            "-r",
            os.path.join(settings.AUDIO_EXTRACTOR_REPO_DIR, "requirements.txt"),
        ]
    )
    print("✅ dependências instaladas")
