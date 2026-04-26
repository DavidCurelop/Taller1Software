"""Implementacion SQLAlchemy del repositorio de productos."""

from sqlalchemy.orm import Session

from src.domain.entities import Product
from src.domain.repositories import IProductRepository
from src.infrastructure.db.models import ProductModel


class SQLProductRepository(IProductRepository):
    """Repositorio concreto de productos usando SQLAlchemy."""

    def __init__(self, db: Session):
        """Inicializa el repositorio con una sesion activa."""
        self.db = db

    def get_all(self) -> list[Product]:
        """Obtiene todos los productos persistidos."""
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(model) for model in models]

    def get_by_id(self, product_id: int) -> Product | None:
        """Obtiene un producto por ID."""
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str) -> list[Product]:
        """Obtiene productos por marca."""
        models = self.db.query(ProductModel).filter(ProductModel.brand.ilike(brand)).all()
        return [self._model_to_entity(model) for model in models]

    def get_by_category(self, category: str) -> list[Product]:
        """Obtiene productos por categoria."""
        models = self.db.query(ProductModel).filter(ProductModel.category.ilike(category)).all()
        return [self._model_to_entity(model) for model in models]

    def save(self, product: Product) -> Product:
        """Guarda o actualiza un producto y retorna la entidad persistida."""
        if product.id is None:
            model = self._entity_to_model(product)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return self._model_to_entity(model)

        model = self.db.query(ProductModel).filter(ProductModel.id == product.id).first()
        if model is None:
            model = self._entity_to_model(product)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return self._model_to_entity(model)

        model.name = product.name
        model.brand = product.brand
        model.category = product.category
        model.size = product.size
        model.color = product.color
        model.price = product.price
        model.stock = product.stock
        model.description = product.description
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def delete(self, product_id: int) -> bool:
        """Elimina un producto por ID."""
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if model is None:
            return False
        self.db.delete(model)
        self.db.commit()
        return True

    @staticmethod
    def _model_to_entity(model: ProductModel) -> Product:
        """Convierte modelo ORM a entidad del dominio."""
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description,
        )

    @staticmethod
    def _entity_to_model(entity: Product) -> ProductModel:
        """Convierte entidad de dominio a modelo ORM."""
        return ProductModel(
            id=entity.id,
            name=entity.name,
            brand=entity.brand,
            category=entity.category,
            size=entity.size,
            color=entity.color,
            price=entity.price,
            stock=entity.stock,
            description=entity.description,
        )
