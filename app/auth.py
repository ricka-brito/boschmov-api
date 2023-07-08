import os
from datetime import datetime, timedelta
from typing import Optional
import pymysql
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from models.user import User, UserCreate
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from models.user import User
from .database import SessionLocal

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = bcrypt.using(rounds=12)

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")


def authenticate_user(session, username: str, password: str):
    user = session.query(User).filter(User.edv == username).first()
    if not user or not pwd_context.verify(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    secret_key = os.environ.get("SECRET_KEY")
    algorithm = "HS256"
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def get_user(username: str):
    with SessionLocal() as session:
        user = session.query(User).filter(User.name == username).first()
        return user

def verify_token(token: str):
    secret_key = os.environ.get("SECRET_KEY")
    algorithm = "HS256"
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    return current_user

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with SessionLocal() as session:
        user = authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid EDV or password")
        token_data = {
            "sub": user.name,
            "admin": user.admin,
        }
        token = create_access_token(token_data)
        return {"access_token": token, "token_type": "bearer"}


@router.post("/create_user")
async def create_user(user: UserCreate, current_user: User = Depends(get_current_admin_user)):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(edv=user.edv, name=user.name, password=hashed_password, admin=user.admin)
    session = SessionLocal()
    session.add(new_user)
    session.commit()

    return {"message": "User created successfully"}


def delete_user_by_edv(session, edv: str):
    user = session.query(User).filter(User.edv == edv).first()
    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/users/{edv}", dependencies=[Depends(get_current_admin_user)])
def delete_existing_user(edv: str):
    with SessionLocal() as session:
        delete_user_by_edv(session, edv)
        return {"message": f"User {edv} deleted successfully"}