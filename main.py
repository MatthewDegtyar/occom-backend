import asyncio
import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import event

from core.db import engine
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


# Load env only for local dev
if os.getenv("ENV") != "PROD":
    load_dotenv()


app = FastAPI()


# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://theoccom.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- Routers ----------------

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


# ---------------- Health ----------------

@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------- Debug (optional) ----------------

async def log_pool_stats():
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
    os.makedirs("./.cache", exist_ok=True)

    # Enable only when actively debugging
    if os.getenv("DEBUG_DB_POOL") == "1":
        asyncio.create_task(log_pool_stats())


# ---------------- SQLAlchemy events (optional) ----------------

@event.listens_for(engine, "checkout")
def checkout(dbapi_conn, conn_record, conn_proxy):
    if os.getenv("DEBUG_DB_POOL") == "1":
        print("CHECKOUT", id(dbapi_conn))


@event.listens_for(engine, "checkin")
def checkin(dbapi_conn, conn_record):
    if os.getenv("DEBUG_DB_POOL") == "1":
        print("CHECKIN", id(dbapi_conn))
