import asyncio
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event

from core.deps import get_db
from models import Base

from routes.colleges import router as colleges_router
from routes.college_yearly_data import router as college_yearly_data_router
from routes.departments import router as departments_router
from routes.professors import router as professors_router
from routes.publications import router as publications_router
from routes.courses import router as courses_router
from routes.course_sections import router as course_sections_router
from routes.textbooks import router as textbooks_router
from routes.library_yearly_data import router as library_yearly_data_router
from routes.vector_search import router as vector_search_router

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/testdb"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_size=100,
    max_overflow=0,
    pool_timeout=30,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

app = FastAPI()

app.add_middleware( # TODO: pull config from .env 
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static/syllabi",
    StaticFiles(directory="./static/syllabi"),
    name="syllabi"
)

app.include_router(colleges_router)
app.include_router(college_yearly_data_router)
app.include_router(departments_router)
app.include_router(professors_router)
app.include_router(publications_router)
app.include_router(courses_router)
app.include_router(course_sections_router)
app.include_router(textbooks_router)
app.include_router(library_yearly_data_router)
app.include_router(vector_search_router)

@app.get("/health") # MUST BE /health FOR EC2 TARGET GROUP CONFIG
def health():
    return {"status": "ok"}

async def log_pool_stats(): # debug number of mysql conncetions
    while True:
        pool = engine.pool
        print(
            f"checked_out={pool.checkedout()} "
            f"size={pool.size()} "
            f"overflow={pool.overflow()}"
        )
        await asyncio.sleep(10)

@app.on_event("startup")
async def startup():
    os.makedirs("./.cache", exist_ok=True) # ensure critical dirs exist for routes/vector_search.py
    #asyncio.create_task(log_pool_stats())
    Base.metadata.create_all(bind=engine)

### mysql connection debug ###
@event.listens_for(engine, "checkout")
def checkout(dbapi_conn, conn_record, conn_proxy):
    print("CHECKOUT", id(dbapi_conn))

@event.listens_for(engine, "checkin")
def checkin(dbapi_conn, conn_record):
    print("CHECKIN", id(dbapi_conn))
### ###