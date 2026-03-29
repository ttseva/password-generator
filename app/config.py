from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = 8000
    host: str = "0.0.0.0"

    database_url: str = "sqlite:///./passwords.db"

    default_length: int = 16
    include_digits: bool = True
    include_specials: bool = True

    class Config:
        env_file = ".env"


settings = Settings()