# Database Schema Documentation

## Overview

This directory contains the complete database schema, migrations, and seed data for the SMB Financial Management System.

**Database**: PostgreSQL 15+  
**Total Tables**: 14  
**Relationships**: Fully normalized with foreign key constraints

---

## Files

- **`init.sql`** - Complete database schema with all tables, indexes, triggers, and constraints
- **`seeds.sql`** - Sample data for development and testing
- **`migrations/`** - Database migration files for version control

---

## Database Structure

### Core Tables

#### Authentication & Users
- `roles` - User roles (admin, accountant, salesperson)
- `users` - System users with authentication

#### Business Entities
- `clients` - Customer database
- `suppliers` - Supplier/vendor database
- `products` - Product and service catalog

#### Transactions
- `purchases` + `purchase_items` - Purchase orders
- `sales` + `sale_items` - Sales orders
- `invoices` + `invoice_items` - General invoices with OCR support
- `income` - Income transactions
- `expenses` - Expense transactions
- `inventory_movements` - Stock movements

---

## Entity Relationships

```
users (1) ----< (*) purchases
users (1) ----< (*) sales
users (1) ----< (*) invoices
users (1) ----< (*) income
users (1) ----< (*) expenses

roles (1) ----< (*) users

clients (1) ----< (*) sales
clients (1) ----< (*) invoices (income type)
clients (1) ----< (*) income

suppliers (1) ----< (*) purchases
suppliers (1) ----< (*) invoices (expense type)
suppliers (1) ----< (*) expenses

products (1) ----< (*) purchase_items
products (1) ----< (*) sale_items
products (1) ----< (*) invoice_items
products (1) ----< (*) inventory_movements

purchases (1) ----< (*) purchase_items
sales (1) ----< (*) sale_items
invoices (1) ----< (*) invoice_items
```

---

## Setup Instructions

### Initial Database Creation

```bash
# Create database
createdb smb_financial_management

# Run schema
psql smb_financial_management < init.sql

# Load seed data (optional)
psql smb_financial_management < seeds.sql
```

### Docker Setup

```bash
# Using docker-compose (see backend/docker-compose.yml)
docker-compose up -d postgres

# Initialize database
docker-compose exec postgres psql -U postgres -d smb_financial_management -f /docker-entrypoint-initdb.d/init.sql
```

---

## Default Users

After running `seeds.sql`, the following users are available:

| Username   | Email                  | Password   | Role        |
|------------|------------------------|------------|-------------|
| admin      | admin@company.com      | admin123   | Admin       |
| contador   | contador@company.com   | admin123   | Accountant  |
| vendedor   | vendedor@company.com   | admin123   | Salesperson |

⚠️ **Security Warning**: Change these passwords in production!

---

## Key Features

### Automated Timestamps
All tables with `updated_at` columns have triggers that automatically update the timestamp on modification.

### Data Integrity
- Foreign key constraints ensure referential integrity
- Check constraints validate data (e.g., invoice type)
- Unique constraints prevent duplicates
- NOT NULL constraints for required fields

### Performance
- Indexes on frequently queried columns
- Indexes on foreign keys for JOIN performance
- Composite indexes on reference fields

### Flexibility
- Support for both income and expense invoices
- Flexible inventory movement tracking
- Extensible category system

---

## Common Queries

### Get user with role
```sql
SELECT u.*, r.name as role_name 
FROM users u 
JOIN roles r ON u.role_id = r.id 
WHERE u.email = 'admin@company.com';
```

### Get sales with client details
```sql
SELECT s.*, c.name as client_name, u.username as created_by
FROM sales s
JOIN clients c ON s.client_id = c.id
JOIN users u ON s.user_id = u.id
ORDER BY s.sale_date DESC;
```

### Get current inventory
```sql
SELECT p.name, p.sku, p.stock_quantity, p.min_stock_level,
       CASE 
           WHEN p.stock_quantity <= p.min_stock_level THEN 'Low Stock'
           ELSE 'OK'
       END as status
FROM products p
WHERE p.is_active = TRUE
ORDER BY p.stock_quantity ASC;
```

### Monthly sales report
```sql
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    COUNT(*) as total_sales,
    SUM(total) as total_revenue
FROM sales
WHERE sale_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', sale_date)
ORDER BY month DESC;
```

---

## Maintenance

### Backup
```bash
pg_dump smb_financial_management > backup_$(date +%Y%m%d).sql
```

### Restore
```bash
psql smb_financial_management < backup_20241208.sql
```

---

## Migration Strategy

Migrations are located in `migrations/` directory and should be:
1. Numbered sequentially (001, 002, etc.)
2. Include up and down scripts
3. Applied in order
4. Tracked in a migrations table (future enhancement)

---

## Database Agent - Deliverable Complete ✓

This schema provides:
- Full relational integrity
- ACID compliance for financial data
- Scalable structure for SMB growth
- Comprehensive indexing for performance
- Sample data for immediate testing
