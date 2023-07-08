from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_admin_user, get_current_user
from app.database import SessionLocal
from sqlalchemy.orm import Session
from models.schemas import BusCreate, Bus
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

@router.get("/busses/{lineNumber}", tags=["Bus Endpoints"])
async def get_bus(lineNumber: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bus = crud.get_bus(lineNumber=lineNumber, db=db)
    if bus is None: 
        raise HTTPException(status_code=404, detail="Bus was not found")
    return bus

@router.get("/busses", tags=["Bus Endpoints"])
async def get_busses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_busses(db=db)

@router.get("/morning/busses", tags=["Bus Endpoints"])
async def get_morning_busses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_morning_busses(db=db)

@router.get("/afternoon/busses", tags=["Bus Endpoints"])
async def get_afternoon_busses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_afternoon_busses(db=db)

@router.post("/admin/busses", tags=["Bus Endpoints"])
async def add_bus(bus: BusCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud.create_bus(db=db, bus=bus)

@router.delete("/admin/busses/{lineNumber}", tags=["Bus Endpoints"])
async def delete_bus(lineNumber: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    deleted= crud.delete_bus(lineNumber=lineNumber, db=db)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Bus was not found")
    return deleted

