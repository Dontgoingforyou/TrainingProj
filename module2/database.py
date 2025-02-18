import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from module2.base import Base

load_dotenv()

POSTGRES_NAME = os.getenv("POSTGRES_NAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"
ADMIN_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/postgres"

admin_engine = create_engine(ADMIN_DATABASE_URL)

with admin_engine.connect() as conn:
    conn.execution_options(isolation_level="AUTOCOMMIT")
    db_exists = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{POSTGRES_NAME}'")).scalar()
    if not db_exists:
        conn.execute(text(f"CREATE DATABASE {POSTGRES_NAME}"))

engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db():
    Base.metadata.create_all(engine)

