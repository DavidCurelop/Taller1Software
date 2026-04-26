"""Configuracion de SQLAlchemy y ciclo de vida de base de datos."""

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import settings


Path("data").mkdir(parents=True, exist_ok=True)

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    """Entrega una sesion de base de datos para dependencias de FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Crea tablas e inserta datos iniciales cuando aplica."""
    from src.infrastructure.db import models
    from src.infrastructure.db.init_data import load_initial_data

    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        load_initial_data(db)
    finally:
        db.close()
