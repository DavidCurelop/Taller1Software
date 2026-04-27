"""Aplicacion FastAPI para el e-commerce con chat IA."""

from datetime import UTC, datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.application.chat_service import ChatService
from src.application.dtos import ChatHistoryDTO, ChatMessageRequestDTO, ChatMessageResponseDTO, ProductDTO
from src.application.product_service import ProductService
from src.domain.exceptions import ChatServiceError, ProductNotFoundError
from src.infrastructure.db.database import get_db, init_db
from src.infrastructure.llm_providers.gemini_service import GeminiService
from src.infrastructure.repositories.chat_repository import SQLChatRepository
from src.infrastructure.repositories.product_repository import SQLProductRepository


app = FastAPI(
    title="E-commerce Chat AI API",
    description="API REST para gestion de productos y chat inteligente de zapatos.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Inicializa base de datos y datos semilla al arrancar la API."""
    init_db()


@app.get("/")
def root() -> RedirectResponse:
    """Redirige a la documentacion interactiva de la API."""
    return RedirectResponse(url="/docs", status_code=307)


@app.get("/products", response_model=list[ProductDTO])
def get_products(
    brand: str | None = Query(default=None, description="Filtrar por marca exacta"),
    category: str | None = Query(default=None, description="Filtrar por categoria exacta"),
    available: bool | None = Query(default=None, description="Filtrar por disponibilidad"),
    db: Session = Depends(get_db),
) -> list[ProductDTO]:
    """Obtiene productos, con filtros opcionales por marca, categoria y disponibilidad."""
    service = ProductService(SQLProductRepository(db))
    if brand is None and category is None and available is None:
        return service.get_all_products()

    return service.search_products(
        {
            "brand": brand,
            "category": category,
            "available": available,
        }
    )


@app.get("/products/{product_id}", response_model=ProductDTO)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductDTO:
    """Obtiene un producto por ID."""
    service = ProductService(SQLProductRepository(db))
    try:
        return service.get_product_by_id(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/chat", response_model=ChatMessageResponseDTO)
async def process_chat_message(
    request: ChatMessageRequestDTO,
    db: Session = Depends(get_db),
) -> ChatMessageResponseDTO:
    """Procesa un mensaje de chat y retorna respuesta del asistente."""
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    ai_service = GeminiService()
    service = ChatService(product_repo=product_repo, chat_repo=chat_repo, ai_service=ai_service)

    try:
        return await service.process_message(request)
    except ChatServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/chat/history/{session_id}", response_model=list[ChatHistoryDTO])
def get_chat_history(
    session_id: str,
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[ChatHistoryDTO]:
    """Obtiene historial de mensajes de una sesion."""
    service = ChatService(
        product_repo=SQLProductRepository(db),
        chat_repo=SQLChatRepository(db),
        ai_service=GeminiService(),
    )
    return service.get_session_history(session_id=session_id, limit=limit)


@app.delete("/chat/history/{session_id}")
def clear_chat_history(session_id: str, db: Session = Depends(get_db)) -> dict:
    """Elimina historial de una sesion y retorna total eliminado."""
    service = ChatService(
        product_repo=SQLProductRepository(db),
        chat_repo=SQLChatRepository(db),
        ai_service=GeminiService(),
    )
    deleted_count = service.clear_session_history(session_id)
    return {"session_id": session_id, "deleted_messages": deleted_count}


@app.get("/health")
def health() -> dict:
    """Endpoint de salud para monitoreo basico."""
    return {"status": "ok", "timestamp": datetime.now(UTC).isoformat()}
