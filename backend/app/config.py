from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    assemblyai_api_key: str
    database_role: str
    database_password: str
    database_region: str
    database_host: str
    database_name: str
    LANGSMITH_TRACING: bool
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str
    class Config:
        env_file = ".env"
    

settings=Settings()

