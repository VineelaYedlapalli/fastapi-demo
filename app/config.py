from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "FastAPI Demo"
    app_version: str = "0.5.0"
    debug: bool = False
    api_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()