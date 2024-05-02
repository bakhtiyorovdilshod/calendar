from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    AUTH_HOST: str
    AUTH_PORT: str
    AUTH_INTERNAL_USERNAME: str
    AUTH_INTERNAL_PASSWORD: str
    AUTH_USE_TLS: bool

    class Config:
        env_prefix = ""


def load_config_from_env():
    config = {}
    for field in Settings.model_fields.keys():
        env_var = os.environ.get(field)
        if env_var is not None:
            config[field] = env_var

    return Settings(**config)


settings = load_config_from_env()
