from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    DATABASE_URL: str
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    TAVILY_API_KEY: Optional[str] = None
    
    CHROMA_SERVER_HOST: str = "localhost"
    CHROMA_SERVER_HTTP_PORT: int = 8000
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma"

    PROJECT_NAME: str = "MemoryOS"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
