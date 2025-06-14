from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    kafka_bootstrap_servers: str
    provider: str = "finnhub"
    symbols: list[str] = ["AAPL", "MSFT"]
    interval: int = 60
    finnhub_api_key: str

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()