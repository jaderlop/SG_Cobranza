# SMB Financial Management System
## Sistema de Gestión Financiera para PyMEs

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Complete web-based financial management application designed for small and medium-sized businesses (PyMEs). Features comprehensive accounting, inventory management, invoice processing with OCR, and financial reporting.

---

## ✨ Features

### Core Functionality
- 🔐 **User Authentication** - JWT-based auth with role-based access control (Admin, Accountant, Salesperson)
- 👥 **Client & Supplier Management** - Complete CRUD operations with contact and payment terms
- 📦 **Product Catalog** - Inventory tracking with stock alerts and pricing
- 💰 **Sales & Purchases** - Order management with line items and status tracking
- 📄 **Invoice Management** - Upload invoice photos with automatic OCR data extraction
- 📊 **Financial Tracking** - Income and expense categorization
- 📈 **Dashboard** - Real-time metrics with interactive charts
- 📑 **Reports** - Financial reports with PDF and Excel export
- 🔍 **OCR Processing** - Automatic invoice data extraction using Tesseract

### Technical Features
- RESTful API with automatic OpenAPI/Swagger documentation
- Server-side rendering with Next.js 14
- Responsive design with TailwindCSS
- Type-safe development with TypeScript
- PostgreSQL database with ACID compliance
- Comprehensive unit testing

---

## 🏗️ Architecture

### Technology Stack

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL 15+
- SQLAlchemy 2.0
- JWT Authentication
- Tesseract OCR
- Alembic (migrations)

**Frontend:**
- Next.js 14 (App Router)
- React 18
- TypeScript
- TailwindCSS
- Chart.js
- Axios + SWR

**DevOps:**
- Docker & Docker Compose
- pytest (backend testing)
- Jest (frontend testing)

---

## 📁 Project Structure

```
SG_gastos/
├── backend/          # FastAPI application
├── frontend/         # Next.js application
├── database/         # SQL schemas and migrations
├── docs/             # Documentation
├── scripts/          # Deployment and utility scripts
└── estructura_proyecto.txt  # Complete project structure
```

See [`estructura_proyecto.txt`](./estructura_proyecto.txt) for the complete directory tree.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 15+**
- **Tesseract OCR**
- **Docker** (optional but recommended)

### Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd SG_gastos
```

#### 2. Database Setup

```bash
# Create database
createdb smb_financial_management

# Initialize schema
psql smb_financial_management < database/init.sql

# Load sample data (optional)
psql smb_financial_management < database/seeds.sql
```

#### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run backend
uvicorn app.main:app --reload
```

Backend will be available at http://localhost:8000
API docs at http://localhost:8000/api/docs

#### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with API URL

# Run frontend
npm run dev
```

Frontend will be available at http://localhost:3000

---

## 🐳 Docker Setup

```bash
# Start all services
docker-compose up -d

# Initialize database
docker-compose exec postgres psql -U postgres -d smb_financial_management -f /docker-entrypoint-initdb.d/init.sql

# View logs
docker-compose logs -f
```

Services:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- PostgreSQL: localhost:5432

---

## 👤 Default Users

After loading seed data:

| Username   | Password  | Role        | Permissions                          |
|------------|-----------|-------------|--------------------------------------|
| admin      | admin123  | Admin       | Full access to all modules           |
| contador   | admin123  | Accountant  | Financial records and reports        |
| vendedor   | admin123  | Salesperson | Sales, clients, and products only    |

⚠️ **Security Warning:** Change these passwords in production!

---

## 📖 Documentation

- [Backend Documentation](./backend/README.md) - API endpoints, setup, and development
- [Frontend Documentation](./frontend/README.md) - Components, pages, and styling
- [Database Documentation](./database/README.md) - Schema, migrations, and queries
- [Architecture Design](./docs/arquitectura.md) - System architecture and design decisions
- [API Endpoints](./docs/api_endpoints.md) - Complete API documentation
- [User Manual](./docs/manual_usuario.md) - End-user guide
- [Deployment Guide](./docs/guia_despliegue.md) - Production deployment instructions

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:watch
```

---

## 📊 Database Schema

The system uses 14 related tables:

- **Users & Roles** - Authentication and authorization
- **Clients & Suppliers** - Business relationships
- **Products** - Product catalog with inventory
- **Purchases & Sales** - Transaction records
- **Invoices** - Invoice management with OCR support
- **Income & Expenses** - Financial tracking
- **Inventory Movements** - Stock tracking

See [database/README.md](./database/README.md) for the complete ER diagram and schema details.

---

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Current user info

### Core Modules
- `/api/clients` - Client management
- `/api/suppliers` - Supplier management
- `/api/products` - Product catalog
- `/api/sales` - Sales orders
- `/api/purchases` - Purchase orders
- `/api/invoices` - Invoice management with OCR
- `/api/income` - Income tracking
- `/api/expenses` - Expense tracking
- `/api/inventory` - Inventory management
- `/api/reports` - Financial reports
- `/api/dashboard` - Dashboard metrics

Full API documentation: http://localhost:8000/api/docs

---

## 🎨 UI/UX Design

The UI follows modern design principles:

- Clean, professional interface optimized for business use
- Responsive design for desktop and mobile
- Dark sidebar with primary blue accent colors
- Intuitive navigation with clear visual hierarchy
- Interactive charts for data visualization
- Form validation with helpful error messages

### Color Palette

- **Primary**: Blue (#0ea5e9)
- **Success**: Green (#10b981)
- **Warning**: Amber (#f59e0b)
- **Danger**: Red (#ef4444)

---

## 🔒 Security

- Passwords hashed with bcrypt
- JWT tokens with configurable expiration
- Role-based access control (RBAC)
- SQL injection prevention via ORM
- Input validation with Pydantic (backend) and Zod (frontend)
- CORS protection
- HTTPS enforcement in production

---

## 🚢 Deployment

### Development

```bash
# Use the development script
./scripts/start_dev.sh
```

### Production

```bash
# Use the deployment script
./scripts/deploy.sh
```

See [docs/guia_despliegue.md](./docs/guia_despliegue.md) for detailed deployment instructions.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

### Agent Team

This project was designed and implemented by specialized AI agents:

1. **Architecture Agent** - System design and technology selection
2. **Database Agent** - PostgreSQL schema and migrations
3. **Backend Agent** - FastAPI implementation
4. **OCR Agent** - Tesseract OCR integration
5. **Frontend Agent** - Next.js and React development
6. **UI/UX Agent** - Design system and user experience
7. **QA Agent** - Testing and quality assurance
8. **Documentation Agent** - Comprehensive documentation

### Technologies

- FastAPI - Modern Python web framework
- Next.js - React framework for production
- PostgreSQL - Reliable relational database
- Tesseract OCR - Open-source OCR engine
- TailwindCSS - Utility-first CSS framework
- Chart.js - JavaScript charting library

---

## 📞 Support

For support, please:
- Check the documentation in the `/docs` folder
- Review the README files in each module
- Check the API documentation at `/api/docs`
- Open an issue on GitHub

---

## 🗺️ Roadmap

### Version 1.1 (Planned)
- [ ] Mobile app with React Native
- [ ] Advanced reporting with custom date ranges
- [ ] Email notifications for low stock
- [ ] Multi-currency support
- [ ] Recurring invoices
- [ ] Batch invoice upload

### Version 1.2 (Planned)
- [ ] Integration with accounting software
- [ ] API for third-party integrations
- [ ] Advanced analytics with AI insights
- [ ] Multi-company support
- [ ] Audit logging
- [ ] Two-factor authentication

---

**Made with ❤️ by the AI Agent Team**

**Version:** 1.0.0  
**Last Updated:** December 2024


