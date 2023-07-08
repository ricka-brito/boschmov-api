from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_admin_user, get_current_user
from app.database import SessionLocal
from sqlalchemy.orm import Session
from models.schemas import AdressBaseCreate
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

@router.get("/adresses", tags=["Adress Endpoints"])
async def get_adresses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_adresses(db=db)

@router.get("/adresses/{adress_id}", tags=["Adress Endpoints"])
async def get_adress(adress_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    adress = crud.get_adress(db=db, adress_id=adress_id)
    if adress is None: 
        raise HTTPException(status_code=404, detail="Adress was not found.")
    return adress

@router.post("/adresses/closest", tags= ["Adress Endpoints"])
async def closest_busstop(initial_adress: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.closestpoints(initial=initial_adress, db=db)


# add this , current_admin: User = Depends(get_current_admin_user)
@router.post("/admin/adresses", tags=["Adress Endpoints"])
async def add_adress(adress: AdressBaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud.create_adress(db=db, adress=adress)

@router.delete("/admin/adresses/{adress_id}", tags=["Adress Endpoints"])
async def delete_adress(adress_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    deleted = crud.delete_adress(db=db, adress_id=adress_id)
    if deleted is None: 
        raise HTTPException(status_code=404, detail="Adress was not found")
    return deleted
