from pydantic_settings import BaseSettings
from pydantic import Extra
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

class Settings(BaseSettings):
    database_url: str
    kafka_bootstrap_servers: str
    redis_url: str
    finnhub_api_key: str
    provider: str = "finnhub"
    symbols: list[str] = ["AAPL", "MSFT"]
    interval: int = 60

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '../../.env')
        env_file_encoding = 'utf-8'
        extra = Extra.allow  # Allow extra fields in .env

def get_settings():
    return Settings()