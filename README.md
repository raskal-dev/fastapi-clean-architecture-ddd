# 🚀 FastAPI CRUD — Clean Architecture + DDD

Backend API template built with:
- FastAPI
- Clean Architecture
- Domain Driven Design (DDD)
- Async SQLAlchemy
- PostgreSQL
- JWT Authentication

This project is designed to be:
- scalable,
- maintainable,
- testable,
- modular,
- production-ready.

---

# 📦 Tech Stack

## Backend
- Python 3.12+
- FastAPI
- SQLAlchemy Async
- Alembic
- Pydantic v2

## Database
- PostgreSQL

## Authentication
- JWT
- OAuth2

## Testing
- Pytest
- HTTPX
- Faker

## Dev Tools
- Ruff
- Black
- MyPy
- Pre-commit

---

# 🏛️ Architecture

The project follows:
- Clean Architecture
- SOLID principles
- DDD (Domain Driven Design)

---

# 📂 Project Structure

```text id="zjlwmr"
app/
│
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── repositories/
│   ├── services/
│   ├── exceptions/
│   └── enums/
│
├── application/
│   ├── use_cases/
│   ├── dto/
│   ├── interfaces/
│   ├── services/
│   └── mappers/
│
├── infrastructure/
│   ├── database/
│   ├── repositories/
│   ├── security/
│   ├── config/
│   └── external_services/
│
├── presentation/
│   ├── api/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── dependencies/
│   │
│   └── middlewares/
│
├── tests/
│
└── main.py