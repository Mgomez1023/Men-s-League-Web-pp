from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Mens League API'
    app_env: str = 'development'
    database_url: str
    cors_origins: str = 'http://localhost:5173'
    supabase_jwt_secret: str
    admin_emails: str

    @field_validator('admin_emails')
    @classmethod
    def validate_admin_emails(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('ADMIN_EMAILS cannot be empty')
        return value

    @property
    def admin_email_list(self) -> List[str]:
        return [email.strip().lower() for email in self.admin_emails.split(',') if email.strip()]

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(',') if origin.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
