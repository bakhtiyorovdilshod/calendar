from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    SERVER_HOST: str
    SERVER_PORT: str
    POSTGRES_DB: str
    
    class Config:
        env_file = ".env"
