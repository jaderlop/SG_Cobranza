-- =====================================================
-- SMB Financial Management System - Seed Data
-- Database Agent Deliverable
-- =====================================================

-- =====================================================
-- SEED ROLES
-- =====================================================
INSERT INTO roles (name, description) VALUES
    ('admin', 'System administrator with full access'),
    ('accountant', 'Accountant with access to financial records'),
    ('salesperson', 'Sales staff with limited access to sales and clients');

-- =====================================================
-- SEED DEFAULT ADMIN USER
-- Password: admin123 (hashed with bcrypt)
-- =====================================================
INSERT INTO users (username, email, password_hash, role_id, first_name, last_name) VALUES
    ('admin', 'admin@company.com', 'admin123', 1, 'System', 'Administrator'),
    ('contador', 'contador@company.com', 'admin123', 2, 'Maria', 'Gonzalez'),
    ('vendedor', 'vendedor@company.com', 'admin123', 3, 'Carlos', 'Rodriguez');

-- =====================================================
-- SEED SAMPLE CLIENTS
-- =====================================================
INSERT INTO clients (name, tax_id, email, phone, address, city, state, country, postal_code, payment_terms, credit_limit) VALUES
    ('Acme Corporation', 'TAX-001-ACME', 'contact@acme.com', '+1-555-0101', '123 Business St', 'New York', 'NY', 'USA', '10001', 'Net 30', 50000.00),
    ('Global Industries', 'TAX-002-GLOBAL', 'info@globalind.com', '+1-555-0102', '456 Commerce Ave', 'Los Angeles', 'CA', 'USA', '90001', 'Net 45', 75000.00),
    ('Tech Solutions Ltd', 'TAX-003-TECH', 'sales@techsol.com', '+1-555-0103', '789 Innovation Blvd', 'San Francisco', 'CA', 'USA', '94102', 'Net 30', 100000.00),
    ('Retail Partners Inc', 'TAX-004-RETAIL', 'orders@retailpartners.com', '+1-555-0104', '321 Market St', 'Chicago', 'IL', 'USA', '60601', 'Net 15', 25000.00),
    ('Manufacturing Co', 'TAX-005-MFG', 'procurement@mfgco.com', '+1-555-0105', '654 Industrial Dr', 'Detroit', 'MI', 'USA', '48201', 'Net 60', 150000.00);

-- =====================================================
-- SEED SAMPLE SUPPLIERS
-- =====================================================
INSERT INTO suppliers (name, tax_id, email, phone, address, city, state, country, postal_code, payment_terms) VALUES
    ('Office Supplies Pro', 'SUP-001-OFFICE', 'orders@officesuppliespro.com', '+1-555-0201', '111 Supply Lane', 'Dallas', 'TX', 'USA', '75201', 'Net 30'),
    ('Tech Hardware Inc', 'SUP-002-TECH', 'sales@techhw.com', '+1-555-0202', '222 Electronics Way', 'Austin', 'TX', 'USA', '78701', 'Net 45'),
    ('Raw Materials Wholesale', 'SUP-003-RAW', 'info@rawmaterials.com', '+1-555-0203', '333 Warehouse Rd', 'Houston', 'TX', 'USA', '77001', 'Net 60'),
    ('Packaging Solutions', 'SUP-004-PKG', 'contact@packagingsol.com', '+1-555-0204', '444 Box St', 'Miami', 'FL', 'USA', '33101', 'Net 30'),
    ('Utilities & Services', 'SUP-005-UTIL', 'billing@utilities.com', '+1-555-0205', '555 Service Ave', 'Atlanta', 'GA', 'USA', '30301', 'Immediate');

-- =====================================================
-- SEED SAMPLE PRODUCTS
-- =====================================================
INSERT INTO products (name, sku, description, category, price, cost, stock_quantity, unit, min_stock_level) VALUES
    ('Laptop Computer', 'PROD-001', 'High-performance business laptop', 'Electronics', 1200.00, 800.00, 50, 'unit', 10),
    ('Office Chair', 'PROD-002', 'Ergonomic office chair with lumbar support', 'Furniture', 350.00, 200.00, 100, 'unit', 20),
    ('Printer Ink Cartridge', 'PROD-003', 'Black ink cartridge for laser printers', 'Supplies', 45.00, 25.00, 200, 'unit', 50),
    ('Wireless Mouse', 'PROD-004', 'Bluetooth wireless mouse', 'Electronics', 25.00, 12.00, 300, 'unit', 50),
    ('Notebook Set', 'PROD-005', 'Pack of 5 professional notebooks', 'Supplies', 15.00, 8.00, 500, 'pack', 100),
    ('External Hard Drive', 'PROD-006', '2TB portable external storage', 'Electronics', 85.00, 50.00, 75, 'unit', 15),
    ('Desk Lamp', 'PROD-007', 'LED desk lamp with adjustable brightness', 'Furniture', 40.00, 22.00, 150, 'unit', 30),
    ('Coffee Machine', 'PROD-008', 'Commercial coffee maker for office', 'Appliances', 450.00, 280.00, 25, 'unit', 5),
    ('Whiteboard Markers', 'PROD-009', 'Set of 12 dry-erase markers', 'Supplies', 12.00, 6.00, 400, 'set', 80),
    ('Standing Desk', 'PROD-010', 'Electric height-adjustable standing desk', 'Furniture', 650.00, 400.00, 30, 'unit', 5);

-- =====================================================
-- SEED SAMPLE PURCHASE
-- =====================================================
INSERT INTO purchases (purchase_number, supplier_id, user_id, purchase_date, subtotal, tax, total, status) VALUES
    ('PO-2024-001', 2, 1, '2024-01-15', 40000.00, 3200.00, 43200.00, 'completed'),
    ('PO-2024-002', 1, 2, '2024-01-20', 5000.00, 400.00, 5400.00, 'completed');

INSERT INTO purchase_items (purchase_id, product_id, quantity, unit_price, subtotal) VALUES
    (1, 1, 50, 800.00, 40000.00),
    (2, 3, 200, 25.00, 5000.00);

-- =====================================================
-- SEED SAMPLE SALE
-- =====================================================
INSERT INTO sales (sale_number, client_id, user_id, sale_date, subtotal, tax, total, status, payment_status) VALUES
    ('SO-2024-001', 1, 3, '2024-02-01', 36000.00, 2880.00, 38880.00, 'completed', 'paid'),
    ('SO-2024-002', 3, 3, '2024-02-05', 12500.00, 1000.00, 13500.00, 'completed', 'partial');

INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
    (1, 1, 30, 1200.00, 36000.00),
    (2, 2, 25, 350.00, 8750.00),
    (2, 6, 50, 85.00, 4250.00);

-- =====================================================
-- SEED SAMPLE INCOME
-- =====================================================
INSERT INTO income (user_id, client_id, income_date, amount, category, description, source, payment_method) VALUES
    (1, 1, '2024-02-01', 38880.00, 'Sales', 'Payment for SO-2024-001', 'Acme Corporation', 'Bank Transfer'),
    (2, 3, '2024-02-10', 6750.00, 'Sales', 'Partial payment for SO-2024-002', 'Tech Solutions Ltd', 'Check'),
    (1, NULL, '2024-02-15', 5000.00, 'Investment', 'Capital injection', 'Owner Investment', 'Bank Transfer');

-- =====================================================
-- SEED SAMPLE EXPENSES
-- =====================================================
INSERT INTO expenses (user_id, supplier_id, expense_date, amount, category, description, payment_method) VALUES
    (2, 2, '2024-01-15', 43200.00, 'Inventory', 'Purchase of laptops - PO-2024-001', 'Bank Transfer'),
    (2, 1, '2024-01-20', 5400.00, 'Supplies', 'Office supplies - PO-2024-002', 'Credit Card'),
    (1, 5, '2024-02-01', 1200.00, 'Utilities', 'Monthly electricity and internet', 'Auto-debit'),
    (2, NULL, '2024-02-05', 3500.00, 'Salaries', 'Staff salaries for January', 'Bank Transfer'),
    (1, 4, '2024-02-10', 850.00, 'Marketing', 'Promotional materials', 'Credit Card');

-- =====================================================
-- SEED INVENTORY MOVEMENTS
-- =====================================================
INSERT INTO inventory_movements (product_id, movement_type, quantity, movement_date, reference_type, reference_id, user_id, notes) VALUES
    (1, 'in', 50, '2024-01-15', 'purchase', 1, 1, 'Received from PO-2024-001'),
    (3, 'in', 200, '2024-01-20', 'purchase', 2, 2, 'Received from PO-2024-002'),
    (1, 'out', 30, '2024-02-01', 'sale', 1, 3, 'Sold via SO-2024-001'),
    (2, 'out', 25, '2024-02-05', 'sale', 2, 3, 'Sold via SO-2024-002'),
    (6, 'out', 50, '2024-02-05', 'sale', 2, 3, 'Sold via SO-2024-002');

-- =====================================================
-- SEED SAMPLE INVOICE
-- =====================================================
INSERT INTO invoices (invoice_number, invoice_type, supplier_id, user_id, invoice_date, subtotal, tax, total, status, ocr_processed) VALUES
    ('INV-SUPP-001', 'expense', 2, 1, '2024-01-15', 40000.00, 3200.00, 43200.00, 'approved', false),
    ('INV-CLI-001', 'income', 1, NULL, '2024-02-01', 36000.00, 2880.00, 38880.00, 'approved', false);

-- Set client_id for income invoice
UPDATE invoices SET client_id = 1 WHERE invoice_number = 'INV-CLI-001';

INSERT INTO invoice_items (invoice_id, product_id, description, quantity, unit_price, subtotal) VALUES
    (1, 1, 'Laptop Computer - High Performance', 50, 800.00, 40000.00),
    (2, 1, 'Laptop Computer - High Performance', 30, 1200.00, 36000.00);
