import uvicorn
from fastapi import FastAPI
from app.auth import router as auth_router
from app.busses import router as busses_router
from app.busstops import router as busstops_router
from app.adresses import router as adresses_router
from app.lines import router as lines_router
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(busses_router)
app.include_router(busstops_router)
app.include_router(adresses_router)
app.include_router(lines_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)