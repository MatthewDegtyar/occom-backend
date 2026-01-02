from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Textbook
from utils.crud_factory import make_crud

router = APIRouter(prefix="/textbooks", tags=["textbooks"])

crud = make_crud(Textbook)

from core.deps import get_db

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return crud.all(db)

@router.get("/{item_id}")
def get_one(item_id: int, db: Session = Depends(get_db)):
    return crud.get(db, item_id)

@router.get("/isbn/{isbn13}")
def search_by_isbn(isbn13: str, db: Session = Depends(get_db)):
    clean = "".join(c for c in isbn13 if c.isdigit())
    return db.query(Textbook).filter(Textbook.isbn_13.like(f"%{clean}%")).all()

@router.post("/")
def create(data: dict, db: Session = Depends(get_db)):
    return crud.create(db, data)

@router.put("/{item_id}")
def update(item_id: int, data: dict, db: Session = Depends(get_db)):
    return crud.update(db, item_id, data)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return crud.delete(db, item_id)
