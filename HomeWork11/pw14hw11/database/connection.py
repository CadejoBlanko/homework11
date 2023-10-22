from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from env import DB_PASSWORD

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
DATABASE_URL = f"postgresql+psycopg2://postgres:{DB_PASSWORD}@127.0.0.1:5432/postgres"
engine = create_engine(DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()