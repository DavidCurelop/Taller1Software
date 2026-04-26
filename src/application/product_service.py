"""Servicio de aplicacion para casos de uso de productos."""

from typing import Any

from src.application.dtos import ProductDTO
from src.domain.entities import Product
from src.domain.exceptions import InvalidProductDataError, ProductNotFoundError
from src.domain.repositories import IProductRepository


class ProductService:
    """Orquesta operaciones de productos usando un repositorio inyectado."""

    def __init__(self, product_repo: IProductRepository):
        """Inicializa el servicio con un repositorio de productos."""
        self.product_repo = product_repo

    def get_all_products(self) -> list[ProductDTO]:
        """Retorna todos los productos del catalogo."""
        products = self.product_repo.get_all()
        return [ProductDTO.model_validate(product) for product in products]

    def get_product_by_id(self, product_id: int) -> ProductDTO:
        """Obtiene un producto por ID o lanza ProductNotFoundError."""
        product = self.product_repo.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return ProductDTO.model_validate(product)

    def search_products(self, filters: dict[str, Any]) -> list[ProductDTO]:
        """Busca productos por marca, categoria y disponibilidad."""
        products = self.product_repo.get_all()

        brand = filters.get("brand")
        if brand:
            brand_lower = str(brand).strip().lower()
            products = [product for product in products if product.brand.lower() == brand_lower]

        category = filters.get("category")
        if category:
            category_lower = str(category).strip().lower()
            products = [product for product in products if product.category.lower() == category_lower]

        available_filter = filters.get("available")
        if available_filter is not None:
            if available_filter:
                products = [product for product in products if product.is_available()]
            else:
                products = [product for product in products if not product.is_available()]

        return [ProductDTO.model_validate(product) for product in products]

    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """Crea un producto nuevo y retorna su representacion DTO."""
        try:
            product = Product(**product_dto.model_dump())
            product.id = None
            saved = self.product_repo.save(product)
            return ProductDTO.model_validate(saved)
        except ValueError as exc:
            raise InvalidProductDataError(str(exc)) from exc

    def update_product(self, product_id: int, product_dto: ProductDTO) -> ProductDTO:
        """Actualiza un producto existente por ID."""
        if self.product_repo.get_by_id(product_id) is None:
            raise ProductNotFoundError(product_id)

        try:
            updated_entity = Product(id=product_id, **product_dto.model_dump(exclude={"id"}))
            saved = self.product_repo.save(updated_entity)
            return ProductDTO.model_validate(saved)
        except ValueError as exc:
            raise InvalidProductDataError(str(exc)) from exc

    def delete_product(self, product_id: int) -> bool:
        """Elimina un producto y lanza excepcion si no existe."""
        deleted = self.product_repo.delete(product_id)
        if not deleted:
            raise ProductNotFoundError(product_id)
        return True

    def get_available_products(self) -> list[ProductDTO]:
        """Retorna solo productos con stock disponible."""
        products = self.product_repo.get_all()
        available = [product for product in products if product.is_available()]
        return [ProductDTO.model_validate(product) for product in available]
