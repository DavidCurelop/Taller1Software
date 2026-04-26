"""Excepciones especificas del dominio."""


class ProductNotFoundError(Exception):
    """Se lanza cuando se busca un producto inexistente."""

    def __init__(self, product_id: int | None = None):
        message = (
            f"Producto con ID {product_id} no encontrado"
            if product_id is not None
            else "Producto no encontrado"
        )
        super().__init__(message)


class InvalidProductDataError(Exception):
    """Se lanza cuando los datos de producto son invalidos."""

    def __init__(self, message: str = "Datos de producto invalidos"):
        super().__init__(message)


class ChatServiceError(Exception):
    """Se lanza cuando el servicio de chat falla."""

    def __init__(self, message: str = "Error en el servicio de chat"):
        super().__init__(message)
