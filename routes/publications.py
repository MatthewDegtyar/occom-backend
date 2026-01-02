from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Publication
from utils.crud_factory import make_crud

router = APIRouter(prefix="/publications", tags=["publications"])

crud = make_crud(Publication)

from core.deps import get_db

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return crud.all(db)

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
