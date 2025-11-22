import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # TODO: Add configuration options

    # OpenAI API Key
    API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Document types
    ALLOWED_DOCUMENT_TYPES: list[str] = [".pdf", ".xlsx"]

settings = Settings()
