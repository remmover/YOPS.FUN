from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "SECRET_KEY"
    algorithm: str = "HS256"
    small_image_size: int = 100

    postgres_user: str = "POSTGRES_USER"
    postgres_password: str = "POSTGRES_PASSWORD"
    postgres_db: str = "POSTGRES_DB"
    postgres_host: str = "POSTGRES_HOST"
    postgres_port: int = 5433

    redis_host: str = "REDIS_HOST"
    redis_port: int = 6379
    redis_password: str = "REDIS_PASSWORD"

    mail_username: str = "HERO@meta.ua"
    mail_password: str = "HERO_MAILBOX_PASSWORD"
    mail_from: str = "HERO@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"

    cloudinary_name: str = "CLOUDINARY_NAME"
    cloudinary_api_key: str = "CLOUDINARY_API_KEY"
    cloudinary_api_secret: str = "CLOUDINARY_API_SECRET"

    gpt_api_key: str = "GPT_API_KEY"

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


config = Settings()
