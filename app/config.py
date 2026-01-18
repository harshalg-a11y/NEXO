from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "Nexo Super App"
    debug: bool = False
    secret_key: str = Field(..., env="SECRET_KEY")
    session_cookie_name: str = "nexo_session"
    
    # Database settings
    mysql_host: str = Field(default="localhost", env="DB_HOST")
    mysql_port: int = Field(default=3306, env="DB_PORT")
    mysql_user: str = Field(default="root", env="DB_USERNAME")
    mysql_password: str = Field(default="", env="DB_PASSWORD")
    mysql_db: str = Field(default="nexo", env="DB_DATABASE")
    
    # JWT settings
    jwt_secret_key: str = Field(default="", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # OpenAI settings
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-3.5-turbo", env="OPENAI_MODEL")
    
    # Mail settings
    mail_from: str = Field(default="noreply@example.com", env="MAIL_FROM")
    mail_host: str = Field(default="smtp.example.com", env="MAIL_HOST")
    mail_port: int = Field(default=587, env="MAIL_PORT")
    mail_username: str = Field(default="", env="MAIL_USERNAME")
    mail_password: str = Field(default="", env="MAIL_PASSWORD")
    mail_use_tls: bool = Field(default=True, env="MAIL_USE_TLS")
    
    # Nexo Paisa settings
    nexo_paisa_api_key: str = Field(default="", env="NEXO_PAISA_API_KEY")
    nexo_paisa_webhook_secret: str = Field(default="", env="NEXO_PAISA_WEBHOOK_SECRET")

    @property
    def database_url(self) -> str:
        return (
            f"mysql+mysqlconnector://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
        )
    
    @property
    def effective_jwt_secret(self) -> str:
        """Return JWT secret key or fallback to main secret key"""
        return self.jwt_secret_key or self.secret_key

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Allow extra fields from environment
        extra = "ignore"

settings = Settings()