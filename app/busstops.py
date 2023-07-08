from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.orm import Session

from app.auth import get_current_admin_user, get_current_user
from app.database import SessionLocal
from sqlalchemy.orm import Session
from models.schemas import BusstopCreate, Busstop
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

@router.get("/busstops", tags=["Busstop Endpoints"])
async def get_busstops(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_busstops(db=db)


@router.get("/busstops/{busstop_id}", tags=["Busstop Endpoints"])
async def get_busstop(busstop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    busstop = crud.get_busstop(db=db, busstop_id=busstop_id)
    if busstop is None:
        raise HTTPException(status_code=404, detail="Busstop was not found.")
    return busstop

# add this , current_admin: User = Depends(get_current_admin_user)
@router.post("/admin/busstops", tags=["Busstop Endpoints"])
async def add_busstop(busstop: BusstopCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud.create_busstop(db=db, busstop=busstop)

@router.delete("/admin/busstops/{busstop_id}", tags=["Busstop Endpoints"])
async def delete_busstop(busstop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    deleted = crud.delete_busstop(db=db, busstop_id=busstop_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Busstop was not found.")
    return deleted

@router.post("/admin/busstops_adress", tags=["Busstop Endpoints"])
async def associate(busstop_id: int, adress_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    adress_busstop = crud.associate_adress_busstop(db=db, db_busstop_id=busstop_id, adress_id=adress_id)
    if adress_busstop is None: 
        raise HTTPException(status_code=400, detail="Association is not possible. Do you have the correct Ids?")
    return adress_busstop

@router.post("/admin/busstop_bus", tags=["Busstop Endpoints"])
async def associate(busstop_id: int, lineNumber: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    busstop_bus = crud.associate_busstop_bus(db=db, db_busstop_id=busstop_id, db_bus_line_number=lineNumber)
    if busstop_bus is None: 
        raise HTTPException(status_code=400, detail="Association is not possible. Do you have the correct Ids?")
    return busstop_bus


