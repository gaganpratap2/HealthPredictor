from pathlib import Path  #Path helps Python work with folders and file paths.
import os  # os lets Python interact with things related to the operating system.

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


# Project root directory: D:\HealthPredictor
BASE_DIR = Path(__file__).resolve().parents[2]

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")


# Engine communicates with PostgreSQL.
engine = create_engine(DATABASE_URL)


# Create the database tables described by our SQLAlchemy models.
Base.metadata.create_all(bind=engine)


# Creates database sessions for interacting with PostgreSQL.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# Provides a database session to FastAPI.
# The session is automatically closed after use.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()