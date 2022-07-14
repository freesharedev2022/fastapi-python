import os
from dotenv import load_dotenv

from pathlib import Path
import pymysql
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "Fast Demo"
    PROJECT_VERSION: str = "1.0.0"

    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_SERVER: str = os.getenv("DB_SERVER", "127.0.0.1")
    DB_PORT: str = os.getenv("DB_PORT", 3306)
    DB_NAME: str = os.getenv("DB_NAME", "fastapi")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

settings = Settings()