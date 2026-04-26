"""Entidades y value objects del dominio."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    """Entidad que representa un producto en el e-commerce."""

    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self) -> None:
        """Valida reglas de negocio basicas del producto."""
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del producto no puede estar vacio")
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")

    def is_available(self) -> bool:
        """Retorna True si el producto tiene stock disponible."""
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """Reduce el stock si la cantidad es valida y existe inventario suficiente."""
        if quantity <= 0:
            raise ValueError("La cantidad a reducir debe ser positiva")
        if quantity > self.stock:
            raise ValueError("No hay suficiente stock disponible")
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """Aumenta el stock en una cantidad positiva."""
        if quantity <= 0:
            raise ValueError("La cantidad a aumentar debe ser positiva")
        self.stock += quantity


@dataclass
class ChatMessage:
    """Entidad que representa un mensaje de chat."""

    id: Optional[int]
    session_id: str
    role: str
    message: str
    timestamp: datetime

    def __post_init__(self) -> None:
        """Valida consistencia del mensaje de chat."""
        if self.role not in {"user", "assistant"}:
            raise ValueError("El rol debe ser 'user' o 'assistant'")
        if not self.message or not self.message.strip():
            raise ValueError("El mensaje no puede estar vacio")
        if not self.session_id or not self.session_id.strip():
            raise ValueError("El session_id no puede estar vacio")

    def is_from_user(self) -> bool:
        """Indica si el mensaje proviene del usuario."""
        return self.role == "user"

    def is_from_assistant(self) -> bool:
        """Indica si el mensaje proviene del asistente."""
        return self.role == "assistant"


@dataclass
class ChatContext:
    """Value object que encapsula el contexto conversacional."""

    messages: list[ChatMessage]
    max_messages: int = 6

    def get_recent_messages(self) -> list[ChatMessage]:
        """Retorna los ultimos N mensajes segun max_messages."""
        return self.messages[-self.max_messages :]

    def format_for_prompt(self) -> str:
        """Formatea historial para inyectarlo en el prompt del modelo."""
        lines: list[str] = []
        for msg in self.get_recent_messages():
            prefix = "Usuario" if msg.is_from_user() else "Asistente"
            lines.append(f"{prefix}: {msg.message}")
        return "\n".join(lines)
