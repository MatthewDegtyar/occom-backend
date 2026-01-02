from fastapi import HTTPException
from sqlalchemy.orm import Session

def get_db():
    from main import get_db as g
    return next(g())

# creates basic CRUD routes for all sql models (from models.py)
def make_crud(model):
    class CRUD:
        def all(self, db: Session):
            return db.query(model).all()

        def get(self, db: Session, id: int):
            obj = db.query(model).get(id)
            if not obj:
                raise HTTPException(404, f"{model.__name__} not found")
            return obj

        def create(self, db: Session, data: dict):
            obj = model(**data)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj

        def update(self, db: Session, id: int, data: dict):
            obj = self.get(db, id)
            for k, v in data.items():
                setattr(obj, k, v)
            db.commit()
            db.refresh(obj)
            return obj

        def delete(self, db: Session, id: int):
            obj = self.get(db, id)
            db.delete(obj)
            db.commit()
            return {"deleted": True}

    return CRUD()