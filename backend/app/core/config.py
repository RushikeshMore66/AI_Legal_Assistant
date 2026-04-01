from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "JurisFlow"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "changethissecretkeyinproduction!"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    REDIS_URL: str = "redis://localhost:6379/0"
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
    
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
