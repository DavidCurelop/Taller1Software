# E-commerce con Chat IA

## Descripcion
API REST de e-commerce de zapatos con chat inteligente usando Clean Architecture.

## Caracteristicas
- Arquitectura en 3 capas: Domain, Application, Infrastructure.
- CRUD basico de productos.
- Chat conversacional con memoria por `session_id`.
- Integracion con Google Gemini (con fallback local cuando no hay API key).
- Persistencia con SQLite y SQLAlchemy.
- Testing unitario con Pytest.
- Despliegue con Docker y Docker Compose.

## Arquitectura
El proyecto sigue Clean Architecture con separacion de responsabilidades:

```text
Cliente HTTP
	|
	v
Infrastructure (FastAPI, SQLAlchemy, Gemini)
	|
	v
Application (ProductService, ChatService, DTOs)
	|
	v
Domain (Entities, Repository Interfaces, Exceptions)
```

## Estructura
- src/domain: entidades, interfaces y excepciones.
- src/application: DTOs y servicios de casos de uso.
- src/infrastructure: API FastAPI, base de datos, repositorios e integracion IA.
- tests: pruebas unitarias.

## Requisitos previos
- Python 3.10+
- Docker (opcional para ejecucion en contenedor)

## Instalacion local
1. Crear entorno virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
copy .env.example .env
# Edita .env y agrega GEMINI_API_KEY si quieres usar Gemini real
```

4. Ejecutar API:
```bash
uvicorn src.infrastructure.api.main:app --reload
```

## Configuracion
Variables de entorno principales:

- `GEMINI_API_KEY`: API key de Google Gemini.
- `DATABASE_URL`: URL de conexion, por defecto `sqlite:///./data/ecommerce_chat.db`.
- `ENVIRONMENT`: entorno de ejecucion (`development`, `production`, etc.).

Usa `.env.example` como plantilla para crear tu archivo `.env`.

## Uso
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

### Endpoints principales
- GET /products
- GET /products/{product_id}
- POST /chat
- GET /chat/history/{session_id}
- DELETE /chat/history/{session_id}

### Ejemplos de consumo

Listar productos disponibles de marca Nike en categoria Running:

```bash
curl "http://localhost:8000/products?brand=Nike&category=Running&available=true"
```

Enviar mensaje al chat:

```bash
curl -X POST "http://localhost:8000/chat" \
	-H "Content-Type: application/json" \
	-d '{"session_id":"cliente_001","message":"Busco zapatos para correr talla 42"}'
```

## Docker
Ejecutar con Docker Compose:
```bash
docker-compose up --build
```

## Tecnologias
- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- Google Gemini API
- Pytest
- Docker / Docker Compose

## Testing
```bash
pytest -q
```

## Notas de IA
Si `GEMINI_API_KEY` no esta definida o Gemini no esta disponible, el sistema responde con un fallback local para no romper el flujo de chat.

## Autor
Proyecto academico - Universidad EAFIT.
