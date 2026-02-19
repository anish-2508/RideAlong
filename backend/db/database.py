from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

def get_engine():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL not set")
    return create_engine(database_url)

def get_session_local():
    engine = get_engine()
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


Base = declarative_base()
