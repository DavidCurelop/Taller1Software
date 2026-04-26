"""Implementacion SQLAlchemy del repositorio de chat."""

from sqlalchemy.orm import Session

from src.domain.entities import ChatMessage
from src.domain.repositories import IChatRepository
from src.infrastructure.db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    """Repositorio concreto para persistencia de memoria conversacional."""

    def __init__(self, db: Session):
        """Inicializa el repositorio con sesion de base de datos."""
        self.db = db

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Guarda un mensaje y retorna la entidad persistida con ID."""
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(self, session_id: str, limit: int | None = None) -> list[ChatMessage]:
        """Retorna historial de sesion en orden cronologico."""
        base_query = self.db.query(ChatMemoryModel).filter(ChatMemoryModel.session_id == session_id)

        if limit is None:
            models = base_query.order_by(ChatMemoryModel.timestamp.asc()).all()
        else:
            # Selecciona los ultimos N mensajes y luego restaura orden cronologico.
            models = base_query.order_by(ChatMemoryModel.timestamp.desc()).limit(limit).all()
            models.reverse()

        return [self._model_to_entity(model) for model in models]

    def delete_session_history(self, session_id: str) -> int:
        """Elimina historial de una sesion y retorna cantidad de filas."""
        count = self.db.query(ChatMemoryModel).filter(ChatMemoryModel.session_id == session_id).delete()
        self.db.commit()
        return count

    def get_recent_messages(self, session_id: str, count: int) -> list[ChatMessage]:
        """Obtiene los ultimos N mensajes de una sesion en orden cronologico."""
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(count)
            .all()
        )
        models.reverse()
        return [self._model_to_entity(model) for model in models]

    @staticmethod
    def _model_to_entity(model: ChatMemoryModel) -> ChatMessage:
        """Convierte modelo ORM a entidad de dominio."""
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp,
        )

    @staticmethod
    def _entity_to_model(entity: ChatMessage) -> ChatMemoryModel:
        """Convierte entidad de dominio a modelo ORM."""
        return ChatMemoryModel(
            id=entity.id,
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp,
        )
