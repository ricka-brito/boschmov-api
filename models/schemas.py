from datetime import time
from typing import Optional
from pydantic import BaseModel

class BusBase(BaseModel):
    class Config:
        orm_mode = True
class AdressBase(BaseModel): 
    class Config:
        orm_mode = True
class BusstopBase(BaseModel):
    class Config:
        orm_mode = True



class BusCreate(BusBase):
    lineNumber: str
    departureTime: time
    busstops: Optional[list[BusstopBase]] = []

class Bus(BusBase):
    pass


class Busstop(BusstopBase):
    idBusstop: int 
    adress: Optional[AdressBase]
    busses: Optional[list[Bus]] = []
class AdressBaseCreate(AdressBase):
    cep: str
    houseNumber: Optional[int]
    street: str
    neighborhoood: str
    city: str
    busstops: Optional[list[Busstop]] = []

class BusstopCreate(BusstopBase):
    stopNumber: int
    time: time

class BusstopAdressCreate(BusstopBase):
    stopNumber: int
    time: time
    adress: Optional[AdressBaseCreate]







class Adress(AdressBase):
    idAdress: int 

class Line(BaseModel):
    linenumber: str
