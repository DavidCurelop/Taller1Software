"""Carga de datos semilla para el catalogo inicial."""

from sqlalchemy.orm import Session

from src.infrastructure.db.models import ProductModel


def load_initial_data(db: Session) -> None:
    """Inserta productos iniciales cuando la tabla esta vacia."""
    if db.query(ProductModel).count() > 0:
        return

    seed_products = [
        ProductModel(name="Air Zoom Pegasus", brand="Nike", category="Running", size="42", color="Negro", price=120.0, stock=5, description="Zapatilla running con amortiguacion reactiva."),
        ProductModel(name="Ultraboost 21", brand="Adidas", category="Running", size="41", color="Blanco", price=150.0, stock=3, description="Modelo premium para entrenamientos largos."),
        ProductModel(name="Suede Classic", brand="Puma", category="Casual", size="40", color="Azul", price=80.0, stock=10, description="Diseno clasico para uso diario."),
        ProductModel(name="Chuck Taylor", brand="Converse", category="Casual", size="39", color="Rojo", price=65.0, stock=8, description="Iconico estilo urbano y versatil."),
        ProductModel(name="Grand Court", brand="Adidas", category="Casual", size="42", color="Blanco", price=75.0, stock=6, description="Inspirado en tenis clasico con confort diario."),
        ProductModel(name="Air Max Alpha", brand="Nike", category="Training", size="43", color="Gris", price=130.0, stock=4, description="Soporte estable para gimnasio y entrenamiento."),
        ProductModel(name="Gel-Kayano 30", brand="Asics", category="Running", size="42", color="Verde", price=170.0, stock=7, description="Alta estabilidad para corredores pronadores."),
        ProductModel(name="Classic Leather", brand="Reebok", category="Casual", size="41", color="Marron", price=90.0, stock=9, description="Cuero suave y estilo retro elegante."),
        ProductModel(name="Oxford Urban", brand="Clarks", category="Formal", size="42", color="Cafe", price=140.0, stock=5, description="Zapato formal comodo para oficina."),
        ProductModel(name="Monk Strap Elite", brand="Hush Puppies", category="Formal", size="41", color="Negro", price=160.0, stock=2, description="Diseno formal premium para eventos."),
    ]

    db.add_all(seed_products)
    db.commit()
