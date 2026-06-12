from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "local"
    PROJECT_NAME: str = "QCM AI Biosensing API"

    # Database
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_USER: str = "qcm_user"
    DB_PASSWORD: str = "qcm_password"
    DB_NAME: str = "qcm_biosensing"

    # Security
    JWT_SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # API keys
    ROOT_ADMIN_API_KEY: str = "CHANGE_ME_ADMIN_KEY"

    # ML
    MODEL_DIR: str = "models"
    DEFAULT_MODEL_NAME: str = "qcm_rf_model.pkl"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
