from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class DatabaseConfig(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = DatabaseConfig()
