from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings

# entry for SQLite
engine = create_engine(
    get_settings.db_url(), 
    connect_args = {"check_same_thread": False}
    )

# will instantiate later
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )

Base = declarative_base()

