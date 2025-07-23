from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TINY_URL_LEN: int
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
