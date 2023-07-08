from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.orm import Session

from app.auth import get_current_admin_user, get_current_user
from app.database import SessionLocal
from sqlalchemy.orm import Session
from models.schemas import BusstopCreate
from models.user import User
from app import crud

router = APIRouter()

#Dependency 
def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/lines", tags=["Line Endpoints"])
async def get_lines(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_lines(db=db)

@router.get("/lines/{line_number}", tags=["Line Endpoints"])
async def get_line_by_time(line_number: str, morning: bool, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_line(line_number=line_number, db=db, morning=morning)

@router.get("/closest/lines/", tags=["Line Endpoints"])
async def get_closest_line(initial_adress: str,  db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_closest_lines(db=db, initial_adress=initial_adress)