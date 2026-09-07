# 🔥 Bonfire Backend

> High-throughput REST API and streaming ETL data ingestion platform for public transit compliance, traffic infraction auditing, and administrative appeals management.

[![Python 3.14](https://img.shields.io/badge/Python-3.14-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Coverage: 95%](https://img.shields.io/badge/Coverage-95%25-brightgreen.svg?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Type Checked: MyPy](https://img.shields.io/badge/Type%20Checked-MyPy%20Strict-blue.svg?logo=python)](https://mypy-lang.org/)
[![Code Style: Ruff](https://img.shields.io/badge/Code%20Style-Ruff-000000.svg?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)
[![Package Manager: uv](https://img.shields.io/badge/Packaging-Astral%20uv-DE5FE9.svg?logo=astral)](https://docs.astral.sh/uv/)
[![API Spec: OpenAPI 3](https://img.shields.io/badge/API%20Spec-OpenAPI%203%20%2F%20Swagger-85EA2D.svg?logo=swagger&logoColor=black)](http://localhost:5000/apidoc/swagger)
[![Security: Keycloak OIDC](https://img.shields.io/badge/Auth-Keycloak%20OIDC%20%28RS256%29-gray.svg?logo=redhat)](https://www.keycloak.org/)

---

## 📌 Overview

**Bonfire Backend** is an enterprise-grade backend service built to ingest, audit, and manage regulatory data for municipal bus transit systems. It serves as the single source of truth for:

- **Infraction Notices (*Autos de Infração*)**: Tracking penalties, violation codes, dates, concessionaires, and fine values.
- **Administrative Appeals (*Recursos de 1ª e 2ª Instância*)**: Ingesting and auditing formal legal judgments published across administrative gazettes.
- **Transit Operators (*Consórcios & Operadoras*)**: Concessionaire registries and operational assignments.
- **Lines & Fleet (*Linhas & Veículos*)**: Active municipal routes, fleet vehicles, shared line operations, and decommission histories.

The system is designed with **Domain-Driven Design (DDD)** principles, resilient **stream-based ETL ingestion**, and **zero-latency distributed token authentication**.

---

## 🏛️ Architecture & Key Highlights

### 1. Layered Architecture & Domain-Driven Design (DDD)
The codebase enforces strict separation between domain logic, persistence, and HTTP transport:
- **Domain Layer (`domain/`)**: Pure business models implemented via **Pydantic V2**. Employs bidirectional alias mapping (`DomainEntity`), allowing Python code to use clean, canonical `snake_case` attributes while seamlessly interfacing with legacy database column names (`NUM_AI`, `COD_LINH`, `ID_OPERADORA`).
- **Repository Layer (`repositories/`)**: Implements the **Repository Pattern** and **Unit of Work** (`IRepositoryManager`, `IRepositorySession`). Transactions are scoped through context managers ensuring atomic commits and automatic rollbacks on errors.
- **Service Layer (`services/`)**: Encapsulates business logic, data transformation, and application commands (e.g., `UpdateLinhaCommand`, `UpdateVeiculoCommand`), keeping controllers lean.
- **Controllers Layer (`controllers/http/`)**: Versioned HTTP Blueprints (`/v1/...`) with legacy route fallback to ensure zero downtime for legacy consumers.

### 2. Stream-Based Ingestion Engine (ETL Pipeline)
Data ingestion is structured through pipeline streams (`InputStream` $\rightarrow$ `TransformStream` $\rightarrow$ `OutputStream`):
- **Multi-Format Extraction**: Parses tabular data (`CSV`, `XLS/XLSX`) and judicial docx decisions (`DOCX`) with table and text extraction.
- **Batch Processing & Dead Letter Queue (DLQ)**: The [`SyncBatchProcessor`](file:///home/lucaslima/Trabalho/Bonfire/backend/infrastructure/parsers/pyingestion/pubsub.py) ingests records in configurable chunks (e.g., 100 items per transaction). If a batch contains corrupted or unmapped data, items are safely routed to an in-memory **Dead Letter Queue (DLQ)**, preventing complete ingestion failure and providing actionable diagnostics.

### 3. Distributed Authentication (Keycloak OIDC + RS256 JWKS Caching)
- Rather than making an HTTP introspection call to Keycloak on every incoming request, the [`KeyCloakAuthenticator`](file:///home/lucaslima/Trabalho/Bonfire/backend/infrastructure/auth/authenticator.py) fetches Keycloak's JSON Web Key Set (JWKS) and caches it in memory with a 24-hour TTL.
- Incoming Bearer tokens are cryptographically verified locally using asymmetric `RS256` public keys and timestamp checks, providing enterprise-grade security with **zero network latency** per request.

### 4. Interactive OpenAPI 3 / Swagger Documentation
- Built with [SpecTree](https://github.com/0b01001001/spectree) and Pydantic schemas, guaranteeing that incoming payloads are validated at runtime and documentation never drifts from code.
- Fully interactive Swagger UI and ReDoc interfaces available out of the box.

---

## 🛠️ Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Language & Runtime** | Python 3.14+, Waitress WSGI |
| **Framework & API** | Flask, Flask-CORS, SpecTree (OpenAPI 3 / Swagger) |
| **Data Validation & Typing** | Pydantic V2, Pydantic-Settings, MyPy (Strict Mode) |
| **Database & ORM** | SQLAlchemy 2.0, PyMySQL, MariaDB / MySQL, Alembic |
| **Ingestion & Data Science** | PyIngestion, Pandas, OpenPyXL, Python-docx, PyPDF2 |
| **Auth & Cryptography** | Keycloak, PyJWT, Cryptography |
| **Tooling & CI/CD** | Astral uv, Ruff, Pytest, Pytest-cov, Docker, GitHub Actions |

---

## 📂 Project Structure

```
.
├── controllers/
│   └── http/
│       ├── v1/              # Versioned API routes (linha, veiculo, consorcio, etc.)
│       │   └── schemas/     # Pydantic DTOs for request/response serialization
│       ├── app.py           # BonfireApp Flask factory, middlewares, and DI
│       ├── error_handlers.py# Centralized RFC-compliant error mapping
│       └── spec.py          # SpecTree OpenAPI 3 configuration
├── domain/
│   ├── entities/            # Pydantic Domain Entities (AutoInfracao, Linha, etc.)
│   └── exceptions.py        # Core domain exceptions
├── services/
│   ├── commands.py          # Application commands for state mutations
│   ├── factory.py           # ServiceFactory dependency injector
│   └── *_service.py         # Business use-case orchestrators
├── repositories/
│   ├── models/              # SQLAlchemy declarative models
│   ├── interfaces.py        # Abstract Repository & Unit of Work interfaces
│   └── manager.py           # SQLAlchemyRepositoryManager & Session lifecycle
├── infrastructure/
│   ├── auth/                # Keycloak OIDC validator & RS256 local JWKS verification
│   ├── cache/               # In-memory TTL cache
│   ├── parsers/             # PyIngestion streams, batch processor, and DLQ
│   └── config.py            # Pydantic Settings configuration loader
├── alembic/                 # Database schema migrations
├── tools/                   # Shell scripts for linux routines & token generation
├── tests/                   # Pytest test suite (184 unit & integration tests)
├── pyproject.toml           # Unified dependencies, ruff, mypy, and pytest config
└── Dockerfile               # Multi-stage Docker image powered by Astral uv
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.14+**
- **[Astral uv](https://docs.astral.sh/uv/)** (recommended) or `pip`
- **Docker & Docker Compose** (optional)
- **MariaDB / MySQL** instance

---

### 1. Environment Setup

Clone the repository and create your local `.env` file from the provided template:

```bash
cp .env.example .env
```

Edit `.env` with your database and Keycloak credentials:

```env
DB_DRIVER=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=bonfire
DB_USER=bonfire
DB_PASSWORD=your_password

KEYCLOAK_ISSUER=http://localhost:8080
KEYCLOAK_REALM_NAME=bonfire
KEYCLOAK_CLIENT_ID=bonfire
KEYCLOAK_CLIENT_SECRET=your_client_secret
```

---

### 2. Local Installation (using `uv`)

Create a virtual environment and install all dependencies including development tools:

```bash
# Create virtual environment with Python 3.14
uv venv .venv --python 3.14

# Activate environment
source .venv/bin/activate

# Install dependencies in editable mode
uv pip install -e ".[dev]"
```

---

### 3. Database Migrations

Apply Alembic migrations to initialize or upgrade the database schema:

```bash
alembic upgrade head
```

---

### 4. Running the Application

Start the server in debug mode:

```bash
python main.py --port 5000 --debug
```

Or run directly with the production WSGI server (Waitress):

```bash
python main.py --port 5000
```

*The API will be available at `http://localhost:5000`.*

---

## 🐳 Running with Docker

The project includes an optimized `Dockerfile` leveraging Astral `uv` for ultra-fast builds:

```bash
# Build Docker image
docker build -t bonfire-backend .

# Run container
docker run -p 5000:5000 --env-file .env bonfire-backend
```

---

## 🧪 Testing & Code Quality

The project maintains a **strict quality bar** enforced in CI:

```bash
# Run unit & integration tests with coverage report (target >= 80%)
pytest --cov=. --cov-report=term-missing

# Run static type checking across all files
mypy .

# Run linter and formatting checks
ruff check .
ruff format --check .
```

### Test Suite Highlights:
- **180+ tests** executed in **~1.2 seconds**.
- **95% overall code coverage**.
- Isolated tests utilizing dependency injection and in-memory fakes ([`tests/fakes.py`](file:///home/lucaslima/Trabalho/Bonfire/backend/tests/fakes.py)).

---

## 📖 API Documentation & Endpoints

When the application is running, access the interactive OpenAPI documentation:

- **Swagger UI**: [http://localhost:5000/apidoc/swagger](http://localhost:5000/apidoc/swagger)
- **ReDoc**: [http://localhost:5000/apidoc/redoc](http://localhost:5000/apidoc/redoc)
- **OpenAPI JSON**: [http://localhost:5000/apidoc/openapi.json](http://localhost:5000/apidoc/openapi.json)

### Core Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/health` | Application health check | ❌ No |
| `GET` | `/v1/linha` | Retrieve transit lines | ✅ Bearer |
| `POST` | `/v1/linha` | Bulk insert transit lines | ✅ Bearer |
| `PATCH`| `/v1/linha` | Bulk update transit lines | ✅ Bearer |
| `DELETE`| `/v1/linha/{code}`| Delete transit line by line code | ✅ Bearer |
| `GET` | `/v1/veiculo` | Retrieve vehicle fleet | ✅ Bearer |
| `POST` | `/v1/veiculo` | Bulk insert vehicles | ✅ Bearer |
| `PATCH`| `/v1/veiculo` | Bulk update vehicles | ✅ Bearer |
| `GET` | `/v1/consorcio` | Retrieve transit concessionaires | ✅ Bearer |
| `GET` | `/v1/autoinfracao`| Query traffic infraction records | ✅ Bearer |
| `POST` | `/v1/autoinfracao/upload` | Upload and stream ingest infraction spreadsheets (CSV/XLS) | ✅ Bearer |
| `GET` | `/v1/recurso/primeira-instancia` | Query first instance appeal judgments | ✅ Bearer |
| `POST` | `/v1/recurso/primeira-instancia/upload` | Ingest first instance legal DOCX decisions | ✅ Bearer |
| `GET` | `/v1/recurso/segunda-instancia` | Query second instance appeal judgments | ✅ Bearer |
| `POST` | `/v1/recurso/segunda-instancia/upload` | Ingest second instance legal DOCX decisions | ✅ Bearer |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
