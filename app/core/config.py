from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@db:5432/marketdata"
    kafka_bootstrap_servers: str = "kafka:9092"
    provider: str = "finnhub"
    symbols: list[str] = ["AAPL", "MSFT"]
    interval: int = 60
    finnhub_api_key: str

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()