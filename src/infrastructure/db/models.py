"""Modelos ORM de la infraestructura."""

from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from src.infrastructure.db.database import Base


class ProductModel(Base):
    """Modelo ORM para la tabla de productos."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(100), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    size = Column(String(20), nullable=False)
    color = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)


class ChatMemoryModel(Base):
    """Modelo ORM para la memoria conversacional."""

    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC), index=True)
