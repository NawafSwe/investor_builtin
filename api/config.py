from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TWELVE_DATA_API_KEY: str

    class Config:
        env_file = ".env"
