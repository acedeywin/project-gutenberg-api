from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
