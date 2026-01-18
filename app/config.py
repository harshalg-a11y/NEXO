from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "NEXO"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-this-secret-key"
    
    # Database
    database_url: str = "mysql+pymysql://root:password@localhost:3306/nexo_db"
    
    # Session
    session_secret_key: str = "change-this-session-secret"
    session_max_age: int = 3600
    
    # CSRF
    csrf_secret_key: str = "change-this-csrf-secret"
    
    # OpenAI
    openai_api_key: str = ""
    
    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@nexo.com"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
