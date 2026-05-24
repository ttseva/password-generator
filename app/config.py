from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: int = 8000
    host: str = "0.0.0.0"

    database_url: str = "sqlite:///./passwords.db"

    default_length: int = 16
    include_digits: bool = True
    include_specials: bool = True

    app_version: str = "unknown"
    app_env: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
