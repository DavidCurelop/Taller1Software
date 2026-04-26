"""Pruebas unitarias para entidades de dominio."""

from datetime import UTC, datetime

import pytest

from src.domain.entities import ChatContext, ChatMessage, Product


def test_product_validations_raise_for_invalid_price(sample_product: Product) -> None:
    """Verifica que el precio invalido dispare ValueError."""
    with pytest.raises(ValueError):
        Product(
            id=sample_product.id,
            name=sample_product.name,
            brand=sample_product.brand,
            category=sample_product.category,
            size=sample_product.size,
            color=sample_product.color,
            price=0,
            stock=sample_product.stock,
            description=sample_product.description,
        )


def test_product_availability_and_stock_changes(sample_product: Product) -> None:
    """Valida disponibilidad y cambios de stock."""
    assert sample_product.is_available() is True

    sample_product.reduce_stock(2)
    assert sample_product.stock == 3

    sample_product.increase_stock(4)
    assert sample_product.stock == 7


def test_product_reduce_stock_fails_when_insufficient(sample_product: Product) -> None:
    """Valida error cuando se intenta reducir mas stock del disponible."""
    with pytest.raises(ValueError):
        sample_product.reduce_stock(10)


def test_chat_message_validations() -> None:
    """Verifica validaciones de rol, mensaje y sesion."""
    now = datetime.now(UTC)

    with pytest.raises(ValueError):
        ChatMessage(id=None, session_id="s1", role="admin", message="hola", timestamp=now)

    with pytest.raises(ValueError):
        ChatMessage(id=None, session_id="", role="user", message="hola", timestamp=now)

    with pytest.raises(ValueError):
        ChatMessage(id=None, session_id="s1", role="user", message="", timestamp=now)


def test_chat_context_format_for_prompt(sample_messages: list[ChatMessage]) -> None:
    """Verifica formateo de historial para prompt."""
    context = ChatContext(messages=sample_messages, max_messages=2)
    prompt_text = context.format_for_prompt()

    assert "Asistente:" in prompt_text
    assert "Usuario:" in prompt_text
    assert "Busco running" in prompt_text
