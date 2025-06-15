from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    kafka_bootstrap_servers: str
    redis_url: str
    finnhub_api_key: str
    provider: str = "finnhub"

    symbols: list[str] = ["AAPL", "MSFT"]
    interval: int = 60

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()