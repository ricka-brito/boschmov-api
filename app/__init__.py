from .database import SessionLocal, engine
from .auth import router as auth_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(auth_router)


# Create the database tables
def create_tables():
    from ..models import Base
    Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup():
    create_tables()


@app.on_event("shutdown")
async def shutdown():
    SessionLocal.close_all()
