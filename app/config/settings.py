from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str
    REPO_URL: str
    CLONE_DIR: str

    class Config:
        env_file = ".env"


settings = Settings()
