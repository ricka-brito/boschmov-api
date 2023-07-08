from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table, Time
from app.database import Base

busstop_bus = Table("busstop_bus", Base.metadata,
                    Column("idBusStop_Bus", primary_key=True),
                    Column("idBusStop", ForeignKey("busstop.idBusStop")),
                    Column("lineNumberBus", ForeignKey("bus.lineNumber"))
                    )


class Busstop(Base):
    __tablename__ = "busstop"

    idBusStop = Column(Integer, primary_key=True, index=True)
    stopNumber = Column(Integer)
    time = Column(Time)
    idAdress = Column(Integer, ForeignKey('adress.idAdress'))

    adress = relationship("Adress", back_populates="busstops", lazy="joined")
    busses = relationship("Bus", secondary=busstop_bus, back_populates="busstops", lazy="joined")



class Adress(Base):
    __tablename__ = "adress"

    idAdress = Column(Integer, primary_key=True, index=True)
    cep = Column(String)
    houseNumber = Column(Integer)
    street = Column(String)
    neighborhood = Column(String)
    city = Column(String)


    busstops = relationship("Busstop", back_populates="adress", lazy="joined")


class Bus(Base):
    __tablename__ = "bus"

    lineNumber = Column(String, primary_key=True)
    departureTime = Column(Time)

    busstops = relationship("Busstop", secondary=busstop_bus, back_populates="busses", lazy="joined")


