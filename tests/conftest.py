"""Fixtures compartidas para pruebas."""

from datetime import UTC, datetime

import pytest

from src.domain.entities import ChatMessage, Product


@pytest.fixture
def sample_product() -> Product:
    """Crea un producto de prueba valido."""
    return Product(
        id=1,
        name="Air Zoom Pegasus",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=120.0,
        stock=5,
        description="Zapatilla running",
    )


@pytest.fixture
def sample_messages() -> list[ChatMessage]:
    """Crea mensajes de prueba para contexto conversacional."""
    now = datetime.now(UTC)
    return [
        ChatMessage(id=1, session_id="s1", role="user", message="Hola", timestamp=now),
        ChatMessage(id=2, session_id="s1", role="assistant", message="Hola, en que te ayudo?", timestamp=now),
        ChatMessage(id=3, session_id="s1", role="user", message="Busco running", timestamp=now),
    ]
