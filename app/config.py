# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str

    # Automatically load variables from the .env file in the root directory
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Instantiate settings so it can be imported across your app
settings = Settings()