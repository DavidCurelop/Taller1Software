"""Servicio de integracion con Google Gemini."""

from __future__ import annotations

from src.domain.entities import ChatContext, Product

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - depende del entorno
    genai = None

from src.config import settings


class GeminiService:
    """Proveedor de IA que genera respuestas contextuales para el e-commerce."""

    def __init__(self):
        """Configura el cliente Gemini si existe API key disponible."""
        self._api_key = settings.gemini_api_key
        self._model_name = "gemini-2.5-flash"
        self._model = None

        if self._api_key and genai is not None:
            genai.configure(api_key=self._api_key)
            self._model = genai.GenerativeModel(self._model_name)

    async def generate_response(
        self,
        user_message: str,
        products: list[Product],
        context: ChatContext,
    ) -> str:
        """Genera una respuesta usando Gemini o un fallback local."""
        if self._model is None:
            return self._fallback_response(user_message=user_message, products=products)

        prompt = self._build_prompt(user_message=user_message, products=products, context=context)
        try:
            response = self._model.generate_content(prompt)
            text = (response.text or "").strip()
            return text if text else self._fallback_response(user_message=user_message, products=products)
        except Exception:
            return self._fallback_response(user_message=user_message, products=products)

    def format_products_info(self, products: list[Product]) -> str:
        """Formatea productos disponibles para el prompt."""
        if not products:
            return "No hay productos disponibles en este momento."

        lines: list[str] = []
        for product in products:
            lines.append(
                f"- {product.name} | Marca: {product.brand} | Categoria: {product.category} | "
                f"Talla: {product.size} | Color: {product.color} | Precio: ${product.price:.2f} | "
                f"Stock: {product.stock}"
            )
        return "\n".join(lines)

    def _build_prompt(self, user_message: str, products: list[Product], context: ChatContext) -> str:
        """Construye el prompt completo para Gemini."""
        products_info = self.format_products_info(products)
        history = context.format_for_prompt() or "Sin historial previo."

        return f"""
Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.

PRODUCTOS DISPONIBLES:
{products_info}

INSTRUCCIONES:
- Se amigable y profesional.
- Usa el contexto de la conversacion anterior.
- Recomienda productos especificos cuando sea apropiado.
- Menciona precios, tallas y disponibilidad.
- Si no tienes informacion, se honesto.

HISTORIAL:
{history}

Usuario: {user_message}

Asistente:
""".strip()

    def _fallback_response(self, user_message: str, products: list[Product]) -> str:
        """Genera respuesta simple cuando no se puede usar Gemini."""
        available = [product for product in products if product.is_available()]
        if not available:
            return "No tenemos productos disponibles en este momento."

        lowered = user_message.lower()
        candidates = available

        brand_hits = [product for product in candidates if product.brand.lower() in lowered]
        if brand_hits:
            candidates = brand_hits

        category_hits = [product for product in candidates if product.category.lower() in lowered]
        if category_hits:
            candidates = category_hits

        top = candidates[:3]
        options = ", ".join(
            f"{product.name} ({product.brand}) talla {product.size} por ${product.price:.2f}"
            for product in top
        )
        return (
            "Te puedo recomendar estas opciones disponibles: "
            f"{options}. Si quieres, te ayudo a filtrar por talla, marca o categoria."
        )
