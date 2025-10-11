from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Chat Application"
    APP_ENV: str = "dev"
    DATABASE_URL: str
    OPENAI_API_KEY: str
    SESSION_EXPIRE_HOURS: int
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()