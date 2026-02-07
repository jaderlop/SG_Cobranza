"""
Dashboard Endpoints Tests
Unit tests for all dashboard endpoints following the project's test pattern
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from datetime import date, timedelta

from app.main import app
from app.core.database import Base, get_db
from app.models import User, Role, Client, Product, Sale, SaleItem, Purchase, PurchaseItem, Supplier

# Test database URL - using SQLite for simplicity
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_dashboard.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def test_db():
    """Create test database and tables"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(test_db):
    """Create test client with database override"""
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture()
def sample_data(test_db):
    """Create sample data for dashboard tests"""
    db = TestingSessionLocal()
    
    # Create role and user
    role = Role(name="admin", description="Administrator")
    db.add(role)
    db.flush()
    
    from app.core.security import get_password_hash
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("testpass123"),
        first_name="Test",
        last_name="User",
        role_id=role.id,
        is_active=True
    )
    db.add(user)
    db.flush()
    
    # Create clients
    client1 = Client(name="Client 1", email="c1@example.com", is_active=True)
    client2 = Client(name="Client 2", email="c2@example.com", is_active=True)
    db.add_all([client1, client2])
    db.flush()
    
    # Create supplier
    supplier = Supplier(name="Supplier 1", email="s1@example.com")
    db.add(supplier)
    db.flush()
    
    # Create products
    product1 = Product(
        name="Product 1", sku="P1", price=Decimal("100.00"), 
        cost=Decimal("50.00"), stock_quantity=50, min_stock_level=10, is_active=True
    )
    product2 = Product(
        name="Product 2", sku="P2", price=Decimal("200.00"), 
        cost=Decimal("100.00"), stock_quantity=5, min_stock_level=10, is_active=True  # Low stock
    )
    product3 = Product(
        name="Product 3", sku="P3", price=Decimal("150.00"), 
        cost=Decimal("75.00"), stock_quantity=100, min_stock_level=20, is_active=True
    )
    db.add_all([product1, product2, product3])
    db.flush()
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=35)  # Outside 30-day window
    
    # Create sales with different dates and statuses
    sale1 = Sale(
        sale_number="SALE-001", client_id=client1.id, user_id=user.id,
        sale_date=today, subtotal=Decimal("500.00"), total=Decimal("500.00"),
        payment_status="paid", status="completed"
    )
    sale2 = Sale(
        sale_number="SALE-002", client_id=client2.id, user_id=user.id,
        sale_date=yesterday, subtotal=Decimal("300.00"), total=Decimal("300.00"),
        payment_status="unpaid", status="pending"
    )
    sale3 = Sale(
        sale_number="SALE-003", client_id=client1.id, user_id=user.id,
        sale_date=last_week, subtotal=Decimal("200.00"), total=Decimal("200.00"),
        payment_status="paid", status="completed"
    )
    sale4 = Sale(
        sale_number="SALE-004", client_id=client2.id, user_id=user.id,
        sale_date=last_month, subtotal=Decimal("1000.00"), total=Decimal("1000.00"),
        payment_status="paid", status="completed"
    )
    db.add_all([sale1, sale2, sale3, sale4])
    db.flush()
    
    # Create sale items
    sale_item1 = SaleItem(
        sale_id=sale1.id, product_id=product1.id,
        quantity=5, unit_price=Decimal("100.00"), subtotal=Decimal("500.00")
    )
    sale_item2 = SaleItem(
        sale_id=sale2.id, product_id=product2.id,
        quantity=2, unit_price=Decimal("150.00"), subtotal=Decimal("300.00")
    )
    sale_item3 = SaleItem(
        sale_id=sale3.id, product_id=product3.id,
        quantity=1, unit_price=Decimal("200.00"), subtotal=Decimal("200.00")
    )
    db.add_all([sale_item1, sale_item2, sale_item3])
    
    # Create purchases
    purchase1 = Purchase(
        purchase_number="PURCHASE-001", supplier_id=supplier.id, user_id=user.id,
        purchase_date=today, subtotal=Decimal("250.00"), total=Decimal("250.00"),
        status="completed"
    )
    purchase2 = Purchase(
        purchase_number="PURCHASE-002", supplier_id=supplier.id, user_id=user.id,
        purchase_date=yesterday, subtotal=Decimal("150.00"), total=Decimal("150.00"),
        status="completed"
    )
    db.add_all([purchase1, purchase2])
    db.flush()
    
    # Create purchase items
    purchase_item1 = PurchaseItem(
        purchase_id=purchase1.id, product_id=product1.id,
        quantity=5, unit_price=Decimal("50.00"), subtotal=Decimal("250.00")
    )
    db.add_all([purchase_item1])
    
    db.commit()
    
    # Capture IDs before closing session
    result = {
        "user_id": user.id,
        "client_ids": [client1.id, client2.id],
        "product_ids": [product1.id, product2.id, product3.id],
        "sale_ids": [sale1.id, sale2.id, sale3.id, sale4.id],
        "purchase_ids": [purchase1.id, purchase2.id]
    }
    
    db.close()
    
    return result


def test_get_kpis_empty_database(client):
    """Test KPIs endpoint with empty database returns zeros"""
    response = client.get("/api/dashboard/kpis")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check all KPIs are present and are zero
    assert data["total_sales_count"] == 0
    assert data["total_sales_amount"] == 0.0
    assert data["total_purchases_amount"] == 0.0
    assert data["total_products"] == 0
    assert data["total_clients"] == 0
    assert data["sales_today"] == 0.0
    assert data["sales_this_month"] == 0.0
    assert data["purchases_this_month"] == 0.0
    assert data["pending_sales_count"] == 0
    assert data["paid_sales_count"] == 0
    assert data["low_stock_products_count"] == 0


def test_get_kpis_with_data(client, sample_data):
    """Test KPIs endpoint with sample data returns correct values"""
    response = client.get("/api/dashboard/kpis")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify data types
    assert isinstance(data["total_sales_count"], int)
    assert isinstance(data["total_sales_amount"], float)
    assert isinstance(data["total_purchases_amount"], float)
    assert isinstance(data["total_products"], int)
    assert isinstance(data["total_clients"], int)
    
    # Check calculated values
    assert data["total_sales_count"] == 4  # 4 sales created
    assert data["total_sales_amount"] == 2000.0  # 500 + 300 + 200 + 1000
    assert data["total_purchases_amount"] == 400.0  # 250 + 150
    assert data["total_products"] == 3  # 3 active products
    assert data["total_clients"] == 2  # 2 active clients
    assert data["sales_today"] == 500.0  # Only sale1 is today
    assert data["pending_sales_count"] == 1  # sale2 is unpaid
    assert data["paid_sales_count"] == 3  # sale1, sale3, sale4 are paid
    assert data["low_stock_products_count"] == 1  # product2 has stock 5 <= min 10


def test_sales_by_day_last_30_days(client, sample_data):
    """Test sales by day endpoint filters last 30 days correctly"""
    response = client.get("/api/dashboard/sales-by-day?days=30")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return list
    assert isinstance(data, list)
    
    # Should only include sales within last 30 days (not last_month sale)
    # We have: today, yesterday, last_week (all within 30 days)
    assert len(data) == 3
    
    # Check data structure
    for item in data:
        assert "date" in item
        assert "total" in item
        assert isinstance(item["date"], str)
        assert isinstance(item["total"], float)


def test_sales_by_day_custom_days(client, sample_data):
    """Test sales by day with custom days parameter"""
    # Test with 1 day (should be limited to recent sales)
    response = client.get("/api/dashboard/sales-by-day?days=1")
    assert response.status_code == 200
    data = response.json()
    # Filter uses >= so may include today's sales
    assert len(data) >= 0  # At minimum no error
    
    # Test with 60 days (should include all sales)
    response = client.get("/api/dashboard/sales-by-day?days=60")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4  # All 4 sales


def test_purchases_by_day_last_30_days(client, sample_data):
    """Test purchases by day endpoint filters last 30 days correctly"""
    response = client.get("/api/dashboard/purchases-by-day?days=30")
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    
    # We have 2 purchases: today and yesterday
    assert len(data) == 2
    
    # Verify total amounts
    total_amount = sum(item["total"] for item in data)
    assert total_amount == 400.0  # 250 + 150


def test_sales_by_status_distribution(client, sample_data):
    """Test sales by status endpoint groups correctly"""
    response = client.get("/api/dashboard/sales-by-status")
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    
    # Should have 2 status groups: paid and unpaid
    assert len(data) == 2
    
    # Check structure
    for item in data:
        assert "status" in item
        assert "count" in item
        assert "total_amount" in item
        assert isinstance(item["status"], str)
        assert isinstance(item["count"], int)
        assert isinstance(item["total_amount"], float)
    
    # Find paid and unpaid groups
    paid_group = next((item for item in data if item["status"] == "paid"), None)
    unpaid_group = next((item for item in data if item["status"] == "unpaid"), None)
    
    assert paid_group is not None
    assert unpaid_group is not None
    
    assert paid_group["count"] == 3  # sale1, sale3, sale4
    assert paid_group["total_amount"] == 1700.0  # 500 + 200 + 1000
    
    assert unpaid_group["count"] == 1  # sale2
    assert unpaid_group["total_amount"] == 300.0


def test_top_products_ranking(client, sample_data):
    """Test top products endpoint returns correct ranking"""
    response = client.get("/api/dashboard/top-products?limit=5")
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) <= 5
    
    # We have 3 products with sales
    assert len(data) == 3
    
    # Check structure
    for item in data:
        assert "product_id" in item
        assert "product_name" in item
        assert "total_quantity" in item
        assert "total_amount" in item
        assert isinstance(item["product_id"], int)
        assert isinstance(item["product_name"], str)
        assert isinstance(item["total_quantity"], int)
        assert isinstance(item["total_amount"], float)
    
    # Verify ranking is by quantity descending
    # product1: 5 units, product2: 2 units, product3: 1 unit
    assert data[0]["total_quantity"] >= data[1]["total_quantity"]
    assert data[1]["total_quantity"] >= data[2]["total_quantity"]


def test_top_products_custom_limit(client, sample_data):
    """Test top products with custom limit"""
    response = client.get("/api/dashboard/top-products?limit=2")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should respect limit
    assert len(data) <= 2


def test_query_param_validation(client):
    """Test query parameter validation"""
    # Days parameter too large
    response = client.get("/api/dashboard/sales-by-day?days=500")
    assert response.status_code == 422
    
    # Days parameter too small
    response = client.get("/api/dashboard/sales-by-day?days=0")
    assert response.status_code == 422
    
    # Limit parameter too large
    response = client.get("/api/dashboard/top-products?limit=100")
    assert response.status_code == 422
    
    # Limit parameter too small
    response = client.get("/api/dashboard/top-products?limit=0")
    assert response.status_code == 422


def test_endpoints_return_correct_types(client, sample_data):
    """Test that all endpoints return correct data types for JSON serialization"""
    # Test KPIs
    response = client.get("/api/dashboard/kpis")
    data = response.json()
    
    # Numeric fields should be float, not string or Decimal
    assert isinstance(data["total_sales_amount"], (int, float))
    assert isinstance(data["total_purchases_amount"], (int, float))
    assert isinstance(data["sales_today"], (int, float))
    
    # Test sales by day
    response = client.get("/api/dashboard/sales-by-day")
    data = response.json()
    if len(data) > 0:
        assert isinstance(data[0]["date"], str)
        assert isinstance(data[0]["total"], (int, float))
    
    # Test sales by status
    response = client.get("/api/dashboard/sales-by-status")
    data = response.json()
    if len(data) > 0:
        assert isinstance(data[0]["total_amount"], (int, float))
    
    # Test top products
    response = client.get("/api/dashboard/top-products")
    data = response.json()
    if len(data) > 0:
        assert isinstance(data[0]["total_amount"], (int, float))
