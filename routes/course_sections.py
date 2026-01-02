from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import CourseSection
from utils.crud_factory import make_crud

router = APIRouter(prefix="/course_sections", tags=["course_sections"])

crud = make_crud(CourseSection)

from core.deps import get_db

@router.get("/")
def get_all(limit: int | None = None, offset: int = 0, db: Session = Depends(get_db)):
    q = db.query(CourseSection)
    if limit is not None:
        q = q.limit(limit).offset(offset)
    return q.all()

@router.get("/{item_id}")
def get_one(item_id: int, db: Session = Depends(get_db)):
    return crud.get(db, item_id)

@router.post("/")
def create(data: dict, db: Session = Depends(get_db)):
    return crud.create(db, data)

@router.put("/{item_id}")
def update(item_id: int, data: dict, db: Session = Depends(get_db)):
    return crud.update(db, item_id, data)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return crud.delete(db, item_id)
