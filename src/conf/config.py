from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    secret_key: str = "HERO_SECRET_KEY"
    algorithm: str = "HS256"

    postgres_user: str = "HERO_POSTGRES_USER"
    postgres_password: str = "HERO_POSTGRES_PASSWORD"
    postgres_db: str = "HERO_POSTGRES_DB_NAME"
    postgres_host: str = "HERO_DOMAIN_OR_IP_POSTGRES_ADDRESS"
    postgres_port: int = 5423

    redis_host: str = "HERO_DOMAIN_OR_IP_REDIS_ADDRESS"
    redis_port: int = 6379
    redis_password: str = "HERO_REDIS_PASSWORD"

    mail_username: str = "HERO@meta.ua"
    mail_password: str = "HERO_MAILBOX_PASSWORD"
    mail_from: str = "HERO@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"

    cloudinary_name: str = "HERO_CLOUDINARY_IDENT"
    cloudinary_api_key: str = "HERO_CLOUDINARY_KEY"
    cloudinary_api_secret: str = "HERO_CLOUDINARY_SECRET"

    gpt_api_key: str = "HERO_CHATGPT_API_KEY"

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


config = Settings()
