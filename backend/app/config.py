from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TCOC - TON Clash of Clans"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/tcoc"
    BOT_TOKEN: str = "YOUR_BOT_TOKEN"
    TELEGRAM_SECRET: str = "YOUR_TELEGRAM_SECRET"
    SECRET_KEY: str = "YOUR_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TON_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
