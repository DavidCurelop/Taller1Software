"""DTOs de entrada y salida de la capa de aplicacion."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class ProductDTO(BaseModel):
    """DTO para transferencia de datos de productos."""

    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, value: float) -> float:
        """Valida que el precio sea mayor a 0."""
        if value <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return value

    @field_validator("stock")
    @classmethod
    def stock_must_be_non_negative(cls, value: int) -> int:
        """Valida que el stock no sea negativo."""
        if value < 0:
            raise ValueError("El stock no puede ser negativo")
        return value


class ChatMessageRequestDTO(BaseModel):
    """DTO para recibir un mensaje de chat."""

    session_id: str
    message: str

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, value: str) -> str:
        """Valida que el mensaje no este vacio."""
        if not value or not value.strip():
            raise ValueError("El mensaje no puede estar vacio")
        return value.strip()

    @field_validator("session_id")
    @classmethod
    def session_id_not_empty(cls, value: str) -> str:
        """Valida que session_id no este vacio."""
        if not value or not value.strip():
            raise ValueError("El session_id no puede estar vacio")
        return value.strip()


class ChatMessageResponseDTO(BaseModel):
    """DTO para retornar la respuesta de chat."""

    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    """DTO para consultar el historial de chat."""

    id: int
    role: str
    message: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
