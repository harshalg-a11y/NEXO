from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "Nexo Super App"
    debug: bool = False
    secret_key: str = Field(..., env="SECRET_KEY")
    session_cookie_name: str = "nexo_session"
    mysql_host: str = Field(default="localhost", env="DB_HOST")
    mysql_port: int = Field(default=3306, env="DB_PORT")
    mysql_user: str = Field(default="root", env="DB_USERNAME")
    mysql_password: str = Field(default="", env="DB_PASSWORD")
    mysql_db: str = Field(default="nexo", env="DB_DATABASE")

    @property
    def database_url(self) -> str:
        return (
            f"mysql+mysqlconnector://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()