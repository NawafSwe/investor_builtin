from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TWELVE_DATA_API_KEY: str
    DB_HOST: str
    DB_PORT: int
    BROKER_HOST: str
    BROKER_PORT: int
    BROKER_USERNAME: str
    BROKER_PASSWORD: str
    ALERTS_QUEUE: str = "threshold_price_reached_alerts"

    class Config:
        env_file = ".env"
