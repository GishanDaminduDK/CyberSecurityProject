from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL  # Import DB URL

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Function to create database tables automatically
def init_db():
    from app.models import item  # Import your models
    Base.metadata.create_all(bind=engine)  # Auto-create tables
