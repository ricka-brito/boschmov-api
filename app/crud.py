from email.policy import HTTP
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import models, schemas
import datetime
def get_busstop(db: Session, busstop_id: int):
    return db.query(models.Busstop).filter(models.Busstop.idBusStop == busstop_id).first()

def create_busstop(db: Session, busstop:  schemas.BusstopCreate):
    db_busstop = models.Busstop(stopNumber=busstop.stopNumber, time=busstop.time)
    db.add(db_busstop)
    db.commit()
    db.refresh(db_busstop)
    return db_busstop

def get_busstops(db: Session, skip = 0, limit: int = 100):
    return db.query(models.Busstop).offset(skip).limit(limit).all()

def delete_busstop(db: Session, busstop_id: int):
    db_busstop = get_busstop(db=db, busstop_id=busstop_id)
    if db_busstop:
        db.delete(db_busstop)
        db.commit()
        return "deleted succesfully"

def create_adress(db: Session, adress: schemas.AdressBaseCreate):
    db_adress = models.Adress(cep= adress.cep, houseNumber= adress.houseNumber, busstops=adress.busstops, street=adress.street, neighborhood=adress.neighborhoood, city=adress.city)
    db.add(db_adress)
    db.commit()
    db.refresh(db_adress)
    return db_adress

def get_adress(db: Session, adress_id: int):
    return db.query(models.Adress).filter(models.Adress.idAdress == adress_id).first()

def get_adresses(db: Session, skip = 0, limit: int = 100):
    return db.query(models.Adress).offset(skip).limit(limit).all()

def delete_adress(db: Session, adress_id: int):
    db_adress = get_adress(db=db, adress_id=adress_id)
    if db_adress:
        db.delete(db_adress)
        db.commit()
        return "deleted succesfully"
    

def get_bus(db: Session, lineNumber: str):
    return db.query(models.Bus).filter(models.Bus.lineNumber == lineNumber).first()

def get_busses(db: Session, skip = 0, limit: int = 100):
    db_busses =  db.query(models.Bus).offset(skip).limit(limit).all() 
    # if the bus has busstops, order them by the stopnumber
    if db_busses:
        for i in db_busses:
            if i.busstops:
                i.busstops.sort(key=lambda element: element.stopNumber)
    return db_busses

def get_morning_busses(db: Session):
    return db.scalars(select(models.Bus).join(models.Bus.busstops.and_(models.Busstop.time < datetime.time(13,00)))).unique().all()

def get_afternoon_busses(db:Session):
    return db.scalars(select(models.Bus).join(models.Bus.busstops.and_(models.Busstop.time > datetime.time(13,00)))).unique().all()

    

def create_bus(db: Session, bus: schemas.BusCreate):
    db_bus = models.Bus(departureTime=bus.departureTime, lineNumber=bus.lineNumber, busstops=bus.busstops )
    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)
    return db_bus

def delete_bus(db: Session, lineNumber: str):
    db_bus = get_bus(db=db, lineNumber=lineNumber)
    if db_bus:
        db.delete(db_bus)
        db.commit()
        return "deleted succesfully"
    

def get_lines(db: Session, skip = 0, limit: int = 100):
    busses = get_busses(db=db, skip=skip, limit=limit)
    str_list = []
    line_list = []
    for i in busses:
        str_list.append(i.lineNumber)
    lineset = set(str_list)
    for i in lineset:
        line_list.append(schemas.Line(linenumber=i))
    return line_list


def get_line(db: Session, line_number: str, morning: bool):
    db_busses = None
    if morning:
        db_busses = db.scalars(select(models.Bus).join(models.Bus.busstops.and_(models.Bus.lineNumber == line_number).and_(models.Busstop.time < datetime.time(13,00)))).first()
    elif not morning:
        db_busses = db.scalars(select(models.Bus).join(models.Bus.busstops.and_(models.Bus.lineNumber == line_number).and_(models.Busstop.time > datetime.time(13,00)))).first()
    if db_busses:
        if db_busses.busstops:
            db_busses.busstops.sort(key=lambda element: element.stopNumber)
    return db_busses

        
def get_closest_lines(db:Session, initial_adress: str):
    closest_adress_busstop = closestpoints(db=db, initial=initial_adress)
    if closest_adress_busstop is None:
        return None
    closest_lines = closest_adress_busstop["Adress"].busstops[0].busses
    closest_line = closest_lines[0]
    if closest_line is None:
        return None
    return closest_line.lineNumber
    

def associate_adress_busstop(db:Session, db_busstop_id: int, adress_id: int):
    db_busstop = get_busstop(db=db, busstop_id=db_busstop_id)
    db_adress = get_adress(db=db, adress_id=adress_id)
    if db_busstop and db_adress:
        db_busstop.idAdress = adress_id
        db.add(db_busstop)
        db.commit()
        return "associated succesfully"

def associate_busstop_bus(db:Session, db_busstop_id: int, db_bus_line_number:str):
    db_busstop = get_busstop(db=db, busstop_id=db_busstop_id)
    db_bus = get_bus(db=db, lineNumber=db_bus_line_number)
    if db_bus and db_busstop:
        db_bus.busstops.append(db_busstop)
        db.add(db_bus)
        db.commit()
        return "associated sucessfully"

def get_bustops_by_adress(db: Session, adress: models.Adress):
    return db.query(models.Busstop).join(models.Adress).filter(models.Adress.idAdress == adress.idAdress).all()

def get_adress_id(db:Session, adress: schemas.AdressBaseCreate):
    adress = db.scalars(select(models.Adress).filter(models.Adress.cep == adress.cep and models.Adress.city == adress.city and models.Adress.neighborhood == adress.neighborhoood and models.Adress.street == adress.street)).first()
    return adress.idAdress

def closestpoints(db : Session, initial: str):
    bustopsdistances = {}
    points = get_adresses(db=db)
    for i in points:

        body = {
          "origins": [
              {
              "waypoint": {
                "address": initial
                          }
              }
          ],
      "destinations": [
          {
          "waypoint": {
            "address": f"{i.street} {i.houseNumber} {i.neighborhood} {i.city} SP {i.cep}"
                      }
          }
      ]
    }
        response = requests.post('https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix', json=body, headers={"X-Goog-Api-Key": "AIzaSyAFP6mWjy3pM5g0Lm4ZyHcQKEvRxAgPw0c", "X-Goog-FieldMask": "distanceMeters"})
        if len(response.json()[0]) == 0 :
            continue
        distance = response.json()[0].get("distanceMeters")
        bustopsdistances[distance] = {"Adress": i, "distance": distance}
    index = min(bustopsdistances)
    distance_value = bustopsdistances[index]["distance"]
    adress_value = bustopsdistances[index]["Adress"]
    return {
        "distance" : distance_value, "Adress": adress_value
    }

