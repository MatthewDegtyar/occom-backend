from .db import SessionLocal

# keep this function isolated in its own file to prevent circular import errors
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
