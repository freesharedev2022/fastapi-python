from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config import settings
from db.session import engine, SessionLocal
from db.base import Base

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    return app

app = start_application()