"""Pruebas unitarias para servicios de aplicacion."""

import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.chat_service import ChatService
from src.application.dtos import ChatMessageRequestDTO, ProductDTO
from src.application.product_service import ProductService
from src.domain.entities import ChatMessage, Product
from src.domain.exceptions import ProductNotFoundError


def test_product_service_get_product_by_id_raises_when_not_found() -> None:
    """Debe lanzar ProductNotFoundError cuando no existe el producto."""
    repo = MagicMock()
    repo.get_by_id.return_value = None
    service = ProductService(repo)

    with pytest.raises(ProductNotFoundError):
        service.get_product_by_id(999)


def test_product_service_create_product_calls_repository() -> None:
    """Debe crear producto y retornar DTO."""
    repo = MagicMock()
    saved = Product(
        id=1,
        name="Test Shoe",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=100.0,
        stock=4,
        description="desc",
    )
    repo.save.return_value = saved
    service = ProductService(repo)

    dto = ProductDTO(
        name="Test Shoe",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=100.0,
        stock=4,
        description="desc",
    )

    result = service.create_product(dto)

    assert result.id == 1
    repo.save.assert_called_once()


def test_chat_service_process_message_flow() -> None:
    """Debe procesar mensaje, invocar IA y persistir ambos mensajes."""
    product_repo = MagicMock()
    product_repo.get_all.return_value = [
        Product(
            id=1,
            name="Air Zoom",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=5,
            description="desc",
        )
    ]

    chat_repo = MagicMock()
    chat_repo.get_recent_messages.return_value = []
    chat_repo.save_message.side_effect = lambda msg: ChatMessage(
        id=1,
        session_id=msg.session_id,
        role=msg.role,
        message=msg.message,
        timestamp=msg.timestamp,
    )

    ai_service = MagicMock()
    ai_service.generate_response = AsyncMock(return_value="Te recomiendo Air Zoom")

    service = ChatService(product_repo=product_repo, chat_repo=chat_repo, ai_service=ai_service)

    response = asyncio.run(service.process_message(ChatMessageRequestDTO(session_id="u1", message="Busco running")))

    assert response.session_id == "u1"
    assert response.assistant_message == "Te recomiendo Air Zoom"
    assert chat_repo.save_message.call_count == 2


def test_chat_service_get_history_maps_dto() -> None:
    """Debe mapear historial de entidades a DTOs."""
    now = datetime.now(UTC)
    product_repo = MagicMock()
    chat_repo = MagicMock()
    chat_repo.get_session_history.return_value = [
        ChatMessage(id=1, session_id="s1", role="user", message="hola", timestamp=now)
    ]
    service = ChatService(product_repo=product_repo, chat_repo=chat_repo, ai_service=MagicMock())

    history = service.get_session_history("s1", limit=10)

    assert len(history) == 1
    assert history[0].role == "user"
