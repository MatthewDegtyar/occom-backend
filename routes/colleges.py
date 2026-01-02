from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import College
from utils.crud_factory import make_crud

router = APIRouter(prefix="/colleges", tags=["colleges"])

crud = make_crud(College)

from core.deps import get_db

@router.get("/")
def get_colleges(
    search: str | None = None,
    state: str | None = None,
    city: str | None = None,
    limit: int | None = None,
    lat: float | None = None,
    lng: float | None = None,
    radius: float | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(College)

    if search:
        query = query.filter(College.name.ilike(f"%{search}%"))

    if state:
        query = query.filter(College.state == state)

    if city:
        query = query.filter(College.city == city)

    if lat and lng and radius:
        query = query.filter(
            func.sqrt(
                (College.latitude - lat) * (College.latitude - lat) +
                (College.longitude - lng) * (College.longitude - lng)
            ) <= radius
        )

    if limit:
        query = query.limit(limit)

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

