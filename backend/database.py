from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base,Session
from fastapi import Depends
from datetime import datetime


DATABASE_URL = "postgresql+psycopg2://postgres:134679@localhost:5432/GPS"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()