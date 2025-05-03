import os
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Demo App of Linear Clone"
    app_version: str = "0.1.0"
    admin_email: str = "admin@email.com"
    graphql_sandbox: Literal["graphiql", "apollo-sandbox", "pathfinder"] | None = "graphiql"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "postgres"
    postgres_user: str = "postgres"
    postgres_password: str = "password"

    allowed_hosts: list[str] = ["*"]

    # TODO: Make key and iv generate automatically on each server startup
    aes_key: str = os.urandom(32).hex()
    aes_iv: str = os.urandom(16).hex()
    jwt_secret: str = os.urandom(32).hex()
    token_expire_minutes: int = 60 * 24

    @property
    def db_creds(self) -> str:
        return f"{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def async_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_creds}"

    @property
    def sync_db_url(self) -> str:
        return f"postgresql://{self.db_creds}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
print(settings.__dict__)
