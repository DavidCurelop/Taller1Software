"""Interfaces de repositorio del dominio."""

from abc import ABC, abstractmethod
from typing import List, Optional

from .entities import ChatMessage, Product


class IProductRepository(ABC):
    """Contrato para acceso a productos."""

    @abstractmethod
    def get_all(self) -> List[Product]:
        """Obtiene todos los productos."""

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto por ID o None si no existe."""

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """Obtiene productos por marca."""

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """Obtiene productos por categoria."""

    @abstractmethod
    def save(self, product: Product) -> Product:
        """Guarda o actualiza un producto."""

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """Elimina un producto por ID."""


class IChatRepository(ABC):
    """Contrato para almacenamiento de mensajes de chat."""

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Guarda un mensaje en el historial."""

    @abstractmethod
    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        """Obtiene historial de una sesion en orden cronologico."""

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """Elimina historial de sesion y retorna cantidad eliminada."""

    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """Obtiene los ultimos mensajes de una sesion en orden cronologico."""
