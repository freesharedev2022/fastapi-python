from typing import Union

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from core.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user

from db.models import users
from core.hashing import Hasher
from dto.user import User
from dto.token import Token
from dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["user"]
)

@router.post("/register")
def create_user(data: User, db: Session = Depends(get_db)):
    checkUser = db.query(users.User).filter(users.User.email == data.email).first()
    if checkUser:
        return {"code": status.HTTP_400_BAD_REQUEST, "message": "User already exists", "data": None}
    db_user = users.User(email=data.email, name=data.name, hashed_password=Hasher.get_password_hash(data.password), address=data.address)
    db.add(db_user)
    db.commit()
    return {"code": status.HTTP_200_OK, "message": "Success", "data": data}

def authenticate_user(db, email: str, password: str):
    user = db.query(users.User).filter(users.User.email == email).first()
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user

@router.post("/login", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dataUser = {"name": user.name, "id": user.id, "email": user.email, "address": user.address}
    access_token = create_access_token(
        data=dataUser, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": dataUser}

@router.get("/")
def read_user(db: Session = Depends(get_db), from_limit: Union[str, None] = 0, to_limit: Union[str, None] = 10):
    result = db.query(users.User).offset(from_limit).limit(to_limit).all()
    return {"code": status.HTTP_200_OK, "message": "Success", "data": result}

@router.get("/me")
def read_user(current_user: users.User = Depends(get_current_user)):
    return {"code": status.HTTP_200_OK, "message": "Success", "data": current_user}

@router.put("/")
def update_user(current_user: users.User = Depends(get_current_user), db: Session = Depends(get_db),
                data: Union[dict, None] = None):
    db.query(users.User).filter(users.User.id == current_user.id).update(
        {"email": data.email, "name": data.name, "hashed_password": Hasher.get_password_hash(data.name), "address": data.address})
    db.commit()
    result = db.query(users.User).filter(users.User.id == current_user.id).first()
    return {"code": status.HTTP_200_OK, "message": "Success", "data": result}