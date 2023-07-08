from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    iduser = Column(Integer, primary_key=True, index=True)
    edv = Column(Integer)
    name = Column(String(50))
    password = Column(String)
    admin = Column(Boolean, default=False)


class UserCreate(BaseModel):
    edv: int
    name: str
    password: str
    admin: bool
    email: str

