from fastapi import FastAPI
import os
import subprocess
import git
from git.exc import GitCommandError

from app.infrastructure import DatabaseInitializer

# --- config do programa do zfturbo ---
REPO_URL = "https://github.com/ZFTurbo/Music-Source-Separation-Training.git"
CLONE_DIR = "app/msst"  # pasta onde vai clonar

# clona ou puxa o repositório do modelo de música e instala as dependências

def sync_music_model_repo():
    if not os.path.exists(CLONE_DIR):
        print(f"⏬ clonando repo de {REPO_URL} pra pasta '{CLONE_DIR}'...")
        git.Repo.clone_from(REPO_URL, CLONE_DIR)
        print("✅ clonagem feita")

        # instala as dependências que tão no requirements.txt
        print("🔧 instalando dependências do requirements.txt do repo...")
        subprocess.run(["uv", "pip", "install", "-r", os.path.join(CLONE_DIR, "requirements.txt")])
        print("✅ dependências instaladas")
    else:
        print("🔄 repo já existe, tentando puxar atualizações...")

        try:
            repo = git.Repo(CLONE_DIR)
            origin = repo.remotes.origin
            origin.fetch()  # pega os commits novos do remoto
            origin.pull()  # puxa as mudanças pro diretório atual
            print("✅ repo atualizado")
        except GitCommandError as e:
            print(f"⚠️ deu erro ao tentar atualizar o repo: {e}")
            print("fazendo reset total pro que tá no remoto...")
            repo.git.reset('--hard')  # reseta tudo pras últimas alterações do remoto
            origin.pull()  # puxa dnv depois do reset
            print("✅ reset feito e repo atualizado")

    # sempre instala as dependências dps de clonar ou atualizar
    print("🔧 instalando dependências do requirements.txt do repo...")
    subprocess.run(["uv", "pip", "install", "-r", os.path.join(CLONE_DIR, "requirements.txt")])
    print("✅ dependências instaladas")


DatabaseInitializer.run()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    sync_music_model_repo()

@app.get("/")
def root():
    return {"oi": "gagui"}
