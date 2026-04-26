"""Servicio de aplicacion para conversacion asistida por IA."""

from datetime import UTC, datetime

from src.application.dtos import ChatHistoryDTO, ChatMessageRequestDTO, ChatMessageResponseDTO
from src.domain.entities import ChatContext, ChatMessage
from src.domain.exceptions import ChatServiceError
from src.domain.repositories import IChatRepository, IProductRepository


class ChatService:
    """Orquesta el flujo de procesamiento de mensajes de chat con contexto."""

    def __init__(self, product_repo: IProductRepository, chat_repo: IChatRepository, ai_service):
        """Inicializa el servicio de chat con sus dependencias."""
        self.product_repo = product_repo
        self.chat_repo = chat_repo
        self.ai_service = ai_service

    async def process_message(self, request: ChatMessageRequestDTO) -> ChatMessageResponseDTO:
        """Procesa un mensaje de usuario y retorna respuesta del asistente."""
        try:
            products = self.product_repo.get_all()
            history = self.chat_repo.get_recent_messages(request.session_id, count=6)
            context = ChatContext(messages=history, max_messages=6)

            assistant_response = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=context,
            )

            now = datetime.now(UTC)
            user_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="user",
                message=request.message,
                timestamp=now,
            )
            assistant_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="assistant",
                message=assistant_response,
                timestamp=now,
            )

            self.chat_repo.save_message(user_msg)
            self.chat_repo.save_message(assistant_msg)

            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=assistant_response,
                timestamp=now,
            )
        except Exception as exc:  # pragma: no cover - salvaguarda de servicio
            raise ChatServiceError(f"No se pudo procesar el mensaje: {exc}") from exc

    def get_session_history(self, session_id: str, limit: int | None = None) -> list[ChatHistoryDTO]:
        """Obtiene historial de una sesion de chat."""
        history = self.chat_repo.get_session_history(session_id, limit=limit)
        return [
            ChatHistoryDTO(
                id=msg.id or 0,
                role=msg.role,
                message=msg.message,
                timestamp=msg.timestamp,
            )
            for msg in history
        ]

    def clear_session_history(self, session_id: str) -> int:
        """Elimina historial completo de una sesion y retorna cantidad eliminada."""
        return self.chat_repo.delete_session_history(session_id)
