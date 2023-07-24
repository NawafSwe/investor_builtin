from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TWELVE_DATA_API_KEY: str
    DB_HOST: str
    DB_PORT: int

    class Config:
        env_file = ".env"
