from typing import Union

from fastapi import Depends, FastAPI, Request, Form
from sqlalchemy.orm import Session

from config import settings
from db.session import engine, SessionLocal
from db.base import Base
from db.models import users
from core.hashing import Hasher
from dto.user import UserCreate

# Dependency
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

@app.get("/")
def read_root():
    return {"code": 200}

@app.post("/users/create")
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    checkUser = db.query(users.User).filter(users.User.email == data.email).first()
    if checkUser:
        return {"code": 400, "message": "User already exists", "data": None}
    db_user = users.User(email=data.email, name=data.name, hashed_password=Hasher.get_password_hash(data.name), address=data.address)
    db.add(db_user)
    db.commit()
    return {"code": 200, "message": "Success", "data": data}

@app.get("/users")
def read_user(db: Session = Depends(get_db), from_limit: Union[str, None] = 0, to_limit: Union[str, None] = 10):
    result = db.query(users.User).offset(from_limit).limit(to_limit).all()
    return {"code": 200, "message": "Success", "data": result}

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    result = db.query(users.User).filter(users.User.id == user_id).first()
    return {"code": 200, "message": "Success", "data": result}


@app.delete("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    result = db.query(users.User).filter(users.User.id == user_id).delete()
    db.commit()
    return {"code": 200, "message": "Success", "data": result}

@app.put("/users/{user_id}")
def update_user(user_id: int, data: UserCreate, db: Session = Depends(get_db)):
    db.query(users.User).filter(users.User.id == user_id).update(
        {"email": data.email, "name": data.name, "hashed_password": Hasher.get_password_hash(data.name), "address": data.address})
    db.commit()
    result = db.query(users.User).filter(users.User.id == user_id).first()
    return {"code": 200, "message": "Success", "data": result}