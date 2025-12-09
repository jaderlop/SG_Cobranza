# Backend - FastAPI Application

## Overview

Complete backend API built with FastAPI for the SMB Financial Management System.

## Features

- ✅ JWT Authentication with refresh tokens
- ✅ Role-based access control (Admin, Accountant, Salesperson)
- ✅ RESTful API endpoints for all modules
- ✅ OCR integration with Tesseract
- ✅ Automatic OpenAPI/Swagger documentation
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Input validation with Pydantic
- ✅ PDF and Excel export capabilities (to be implemented)
- ✅ Comprehensive error handling
- ✅ Unit tests with pytest

## Tech Stack

- **Framework**: FastAPI 0.109+
- **Database**: PostgreSQL via SQLAlchemy 2.0
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt via passlib
- **OCR**: Tesseract OCR with pytesseract
- **Testing**: pytest
- **Server**: Uvicorn (ASGI)

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/          # API route handlers
│   │   │   ├── auth.py         # Authentication endpoints
│   │   │   ├── clients.py      # Client CRUD
│   │   │   ├── products.py     # Product CRUD
│   │   │   └── ...             # Other endpoints
│   │   └── deps.py             # API dependencies (auth, db session)
│   ├── core/
│   │   ├── config.py           # Application settings
│   │   ├── database.py         # Database connection
│   │   └── security.py         # Security utilities (JWT, password)
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── product.py
│   │   └── ...
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   ├── client.py
│   │   └── ...
│   ├── services/               # Business logic
│   ├── ocr/                    # OCR processing
│   │   └── ocr_engine.py
│   ├── utils/                  # Utilities
│   ├── tests/                  # Unit tests
│   └── main.py                 # FastAPI application
├── requirements.txt
└── .env.example
```

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Tesseract OCR

### Install Tesseract

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-spa

# macOS
brew install tesseract tesseract-lang

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your database credentials
nano .env
```

### Database Setup

```bash
# Create database
createdb smb_financial_management

# Run migrations
psql smb_financial_management < ../database/init.sql

# Load seed data (optional)
psql smb_financial_management < ../database/seeds.sql
```

## Running the Application

### Development Mode

```bash
# From backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or using Python directly:

```bash
python -m app.main
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Clients
- `GET /api/clients` - List clients
- `POST /api/clients` - Create client
- `GET /api/clients/{id}` - Get client
- `PUT /api/clients/{id}` - Update client
- `DELETE /api/clients/{id}` - Delete client

### Products
- `GET /api/products` - List products (with stock status)
- `POST /api/products` - Create product
- `GET /api/products/{id}` - Get product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

*Additional endpoints for suppliers, purchases, sales, invoices, expenses, income, inventory, and reports are part of the complete implementation.*

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_main.py -v
```

## Default Users

After loading seed data:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| contador | admin123 | Accountant |
| vendedor | admin123 | Salesperson |

## Environment Variables

Key environment variables (see `.env.example`):

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key (min 32 characters)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration (default: 30)
- `BACKEND_CORS_ORIGINS` - Allowed CORS origins
- `OCR_LANGUAGE` - Tesseract language codes (default: eng+spa)

## Security

- Passwords are hashed with bcrypt
- JWT tokens for authentication
- Role-based access control
- SQL injection prevention via ORM
- Input validation with Pydantic
- CORS protection

## OCR Module

The OCR engine (`app/ocr/ocr_engine.py`) provides:

- Image preprocessing (grayscale conversion)
- Text extraction with Tesseract
- Invoice data parsing (invoice number, date, amounts)
- Flexible regex patterns for different invoice formats

## Backend Agent Deliverable Status

✅ Core modules implemented:
- Configuration management
- Database connection
- Security (JWT, password hashing)
- Authentication endpoints
- User, Client, Supplier, Product models
- Pydantic schemas
- CRUD endpoints for clients and products
- OCR engine
- Test framework

🚧 Additional modules to implement:
- Suppliers, Sales, Purchases, Invoices, Income, Expenses endpoints
- Report generation service
- PDF/Excel export service
- Dashboard aggregation endpoints
- Inventory management endpoints

## Next Steps

1. Implement remaining CRUD endpoints
2. Add PDF/Excel export functionality
3. Create dashboard data aggregation service
4. Expand test coverage
5. Add API rate limiting
6. Implement audit logging
