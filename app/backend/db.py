from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# двигатель для SQLite
DATABASE_URL = 'sqlite:///taskmanager.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
