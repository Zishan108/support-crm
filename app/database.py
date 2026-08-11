
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./support_crm.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is a factory that creates new DB session objects.
# Each request gets its own session (see get_db() below).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class our table models (models.py) will inherit from.
# SQLAlchemy uses this to know which classes map to which DB tables.
Base = declarative_base()


def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()