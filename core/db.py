from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/testdb"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_size=1,
    max_overflow=0,
    pool_timeout=30
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db():
    Base.metadata.create_all(bind=engine)
