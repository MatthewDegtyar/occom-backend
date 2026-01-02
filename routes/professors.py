from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Professor, College
from utils.crud_factory import make_crud
from sqlalchemy import or_

router = APIRouter(prefix="/professors", tags=["professors"])

crud = make_crud(Professor)

from core.deps import get_db

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return crud.all(db)

@router.get("/search")
def search_professors(school: str = None, name: str = None, db: Session = Depends(get_db)):
    query = db.query(Professor)

    if school:
        if school.isdigit():
            query = query.filter(Professor.college_id == int(school))
        else:
            query = query.join(College).filter(College.name.ilike(f"%{school}%"))

    if name:
        clean = name.strip()
        query = query.filter(
            or_(
                Professor.first_name.ilike(f"%{clean}%"),
                Professor.last_name.ilike(f"%{clean}%")
            )
        )

    return query.all()

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
