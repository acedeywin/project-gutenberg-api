from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str
    OPENAI_API_KEY: str
    LLAMA_API_KEY: str
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
