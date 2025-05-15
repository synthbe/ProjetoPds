from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str
    AUDIO_EXTRACTOR_REPO_URL: str
    AUDIO_EXTRACTOR_REPO_DIR: str

    class Config:
        env_file = ".env"


settings = Settings()
