from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Order Management Service"
    database_url: str
    mongodb_url: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
