from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "NetWatch"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://netwatch_user:netwatch_pass@localhost:5432/netwatch_db"
    
    # JWT
    SECRET_KEY: str = "change-this-to-a-very-long-random-string-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Monitoring
    CHECK_INTERVAL_SECONDS: int = 60
    SSL_EXPIRY_WARNING_DAYS: int = 30

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()