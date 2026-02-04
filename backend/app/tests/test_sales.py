import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from datetime import date, datetime

from app.main import app
from app.core.database import Base, get_db
from app.models import User, Role, Client, Product, Sale, SaleItem

# Test database URL - using SQLite for simplicity
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sales.db"

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
def auth_token(client, test_db):
    """Create a test user and return auth token"""
    db = TestingSessionLocal()
    
    # Create role
    role = Role(name="admin", description="Administrator")
    db.add(role)
    db.flush()
    
    # Create user
    from app.core.security import get_password_hash
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        full_name="Test User",
        role_id=role.id,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.close()
    
    # Login to get token
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture()
def test_client_data(test_db):
    """Create a test client in the database"""
    db = TestingSessionLocal()
    client_obj = Client(
        name="Test Client",
        email="client@example.com",
        phone="1234567890"
    )
    db.add(client_obj)
    db.commit()
    client_id = client_obj.id
    db.close()
    return client_id


@pytest.fixture()
def test_product(test_db):
    """Create a test product in the database"""
    db = TestingSessionLocal()
    product = Product(
        name="Test Product",
        sku="TEST-001",
        price=Decimal("100.00"),
        cost=Decimal("50.00"),
        stock_quantity=100
    )
    db.add(product)
    db.commit()
    product_id = product.id
    db.close()
    return product_id


def test_create_sale_success(client, auth_token, test_client_data, test_product):
    """Test creating a sale with valid data"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    sale_data = {
        "client_id": test_client_data,
        "sale_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 5,
                "unit_price": "100.00"
            }
        ]
    }
    
    response = client.post("/api/v1/sales/", json=sale_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    
    # Check sale fields
    assert data["id"] is not None
    assert data["client_id"] == test_client_data
    assert data["sale_number"] is not None
    assert "SALE-" in data["sale_number"]
    
    # Check calculations
    assert Decimal(str(data["subtotal"])) == Decimal("500.00")  # 5 * 100
    assert Decimal(str(data["total"])) == Decimal("500.00")
    assert Decimal(str(data["tax"])) == Decimal("0.00")
    assert Decimal(str(data["discount"])) == Decimal("0.00")
    
    # Check items
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == test_product
    assert data["items"][0]["quantity"] == 5
    assert Decimal(str(data["items"][0]["unit_price"])) == Decimal("100.00")
    assert Decimal(str(data["items"][0]["subtotal"])) == Decimal("500.00")
    
    # Verify stock was decremented
    db = TestingSessionLocal()
    product = db.query(Product).filter(Product.id == test_product).first()
    assert product.stock_quantity == 95  # 100 - 5
    db.close()


def test_create_sale_empty_items(client, auth_token, test_client_data):
    """Test that creating a sale with no items fails"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    sale_data = {
        "client_id": test_client_data,
        "sale_date": str(date.today()),
        "items": []
    }
    
    response = client.post("/api/v1/sales/", json=sale_data, headers=headers)
    
    # Should fail validation
    assert response.status_code == 422


def test_create_sale_invalid_product(client, auth_token, test_client_data):
    """Test that creating a sale with invalid product fails"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    sale_data = {
        "client_id": test_client_data,
        "sale_date": str(date.today()),
        "items": [
            {
                "product_id": 99999,  # Non-existent product
                "quantity": 5,
                "unit_price": "100.00"
            }
        ]
    }
    
    response = client.post("/api/v1/sales/", json=sale_data, headers=headers)
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_create_sale_insufficient_stock(client, auth_token, test_client_data, test_product):
    """Test that creating a sale with insufficient stock fails"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    sale_data = {
        "client_id": test_client_data,
        "sale_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 1000,  # More than available stock (100)
                "unit_price": "100.00"
            }
        ]
    }
    
    response = client.post("/api/v1/sales/", json=sale_data, headers=headers)
    
    assert response.status_code == 400
    assert "insufficient stock" in response.json()["detail"].lower()


def test_list_sales(client, auth_token, test_client_data, test_product):
    """Test listing all sales"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create a sale first
    sale_data = {
        "client_id": test_client_data,
        "sale_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 2,
                "unit_price": "100.00"
            }
        ]
    }
    client.post("/api/v1/sales/", json=sale_data, headers=headers)
    
    # List sales
    response = client.get("/api/v1/sales/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_sale_by_id(client, auth_token, test_client_data, test_product):
    """Test getting a single sale by ID"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create a sale
    sale_data = {
        "client_id": test_client_data,
        "sale_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 3,
                "unit_price": "100.00"
            }
        ]
    }
    create_response = client.post("/api/v1/sales/", json=sale_data, headers=headers)
    sale_id = create_response.json()["id"]
    
    # Get the sale
    response = client.get(f"/api/v1/sales/{sale_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sale_id
    assert len(data["items"]) == 1


def test_get_sale_not_found(client, auth_token):
    """Test getting a non-existent sale returns 404"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = client.get("/api/v1/sales/99999", headers=headers)
    
    assert response.status_code == 404


def test_update_sale(client, auth_token, test_client_data, test_product):
    """Test updating a sale"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create initial sale
    sale_data = {
        "client_id": test_client_data,
        "sale_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 5,
                "unit_price": "100.00"
            }
        ]
    }
    create_response = client.post("/api/v1/sales/", json=sale_data, headers=headers)
    sale_id = create_response.json()["id"]
    
    # Check initial stock
    db = TestingSessionLocal()
    product = db.query(Product).filter(Product.id == test_product).first()
    stock_after_create = product.stock_quantity
    db.close()
    
    # Update sale with different quantity
    update_data = {
        "items": [
            {
                "product_id": test_product,
                "quantity": 3,  # Changed from 5 to 3
                "unit_price": "100.00"
            }
        ]
    }
    response = client.put(f"/api/v1/sales/{sale_id}", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check updated calculations
    assert Decimal(str(data["subtotal"])) == Decimal("300.00")  # 3 * 100
    assert Decimal(str(data["total"])) == Decimal("300.00")
    
    # Verify stock was adjusted correctly
    # Should have restored 5 and then taken 3, net change: +2
    db = TestingSessionLocal()
    product = db.query(Product).filter(Product.id == test_product).first()
    assert product.stock_quantity == stock_after_create + 2
    db.close()


def test_delete_sale(client, auth_token, test_client_data, test_product):
    """Test deleting a sale"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create a sale
    sale_data = {
        "client_id": test_client_data,
        "sale_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 10,
                "unit_price": "100.00"
            }
        ]
    }
    create_response = client.post("/api/v1/sales/", json=sale_data, headers=headers)
    sale_id = create_response.json()["id"]
    
    # Check stock after creation
    db = TestingSessionLocal()
    product = db.query(Product).filter(Product.id == test_product).first()
    stock_after_create = product.stock_quantity
    db.close()
    
    # Delete the sale
    response = client.delete(f"/api/v1/sales/{sale_id}", headers=headers)
    
    assert response.status_code == 204
    
    # Verify sale is deleted
    get_response = client.get(f"/api/v1/sales/{sale_id}", headers=headers)
    assert get_response.status_code == 404
    
    # Verify stock was restored
    db = TestingSessionLocal()
    product = db.query(Product).filter(Product.id == test_product).first()
    assert product.stock_quantity == stock_after_create + 10  # Stock restored
    db.close()


def test_calculation_accuracy_multiple_items(client, auth_token, test_client_data, test_db):
    """Test that calculations are accurate with multiple items"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create multiple products
    db = TestingSessionLocal()
    product1 = Product(name="Product 1", sku="P1", price=Decimal("50.00"), stock_quantity=100)
    product2 = Product(name="Product 2", sku="P2", price=Decimal("75.50"), stock_quantity=100)
    db.add_all([product1, product2])
    db.commit()
    p1_id = product1.id
    p2_id = product2.id
    db.close()
    
    # Create sale with multiple items
    sale_data = {
        "client_id": test_client_data,
        "sale_date": str(date.today()),
        "items": [
            {
                "product_id": p1_id,
                "quantity": 3,
                "unit_price": "50.00"
            },
            {
                "product_id": p2_id,
                "quantity": 2,
                "unit_price": "75.50"
            }
        ]
    }
    
    response = client.post("/api/v1/sales/", json=sale_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    
    # Check calculations (3*50 + 2*75.50 = 150 + 151 = 301)
    assert Decimal(str(data["subtotal"])) == Decimal("301.00")
    assert Decimal(str(data["total"])) == Decimal("301.00")
    
    # Check individual item subtotals
    items = sorted(data["items"], key=lambda x: x["product_id"])
    assert Decimal(str(items[0]["subtotal"])) == Decimal("150.00")  # 3 * 50
    assert Decimal(str(items[1]["subtotal"])) == Decimal("151.00")  # 2 * 75.50
