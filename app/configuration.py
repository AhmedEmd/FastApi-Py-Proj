from pydantic_settings import BaseSettings
from typing import Optional

class Validation(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_password: str = "ah01011747352"
    database_name: str = "fastapidatabase"
    database_username: str = "postgres"
    secret_key: Optional[str] = None
    algorithm: Optional[str] = None
    access_token_expire_minutes: Optional[int] = None

    class Config:
        env_file = ".env"

settings = Validation()
