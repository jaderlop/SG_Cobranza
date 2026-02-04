import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from datetime import date, datetime

from app.main import app
from app.core.database import Base, get_db
from app.models import User, Role, Supplier, Product, Purchase, PurchaseItem

# Test database URL - using SQLite for simplicity
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_purchases.db"

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
def test_supplier(test_db):
    """Create a test supplier in the database"""
    db = TestingSessionLocal()
    supplier = Supplier(
        name="Test Supplier",
        email="supplier@example.com",
        phone="1234567890"
    )
    db.add(supplier)
    db.commit()
    supplier_id = supplier.id
    db.close()
    return supplier_id


@pytest.fixture()
def test_product(test_db):
    """Create a test product in the database"""
    db = TestingSessionLocal()
    product = Product(
        name="Test Product",
        sku="TEST-001",
        price=Decimal("100.00"),
        cost=Decimal("50.00"),
        stock_quantity=10  # Start with low stock
    )
    db.add(product)
    db.commit()
    product_id = product.id
    db.close()
    return product_id


def test_create_purchase_success(client, auth_token, test_supplier, test_product):
    """Test creating a purchase with valid data"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    purchase_data = {
        "supplier_id": test_supplier,
        "purchase_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 50,
                "unit_price": "45.00"
            }
        ]
    }
    
    response = client.post("/api/v1/purchases/", json=purchase_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    
    # Check purchase fields
    assert data["id"] is not None
    assert data["supplier_id"] == test_supplier
    assert data["purchase_number"] is not None
    assert "PURCHASE-" in data["purchase_number"]
    
    # Check calculations
    assert Decimal(str(data["subtotal"])) == Decimal("2250.00")  # 50 * 45
    assert Decimal(str(data["total"])) == Decimal("2250.00")
    assert Decimal(str(data["tax"])) == Decimal("0.00")
    assert Decimal(str(data["discount"])) == Decimal("0.00")
    
    # Check items
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == test_product
    assert data["items"][0]["quantity"] == 50
    assert Decimal(str(data["items"][0]["unit_price"])) == Decimal("45.00")
    assert Decimal(str(data["items"][0]["subtotal"])) == Decimal("2250.00")
    
    # Verify stock was incremented
    db = TestingSessionLocal()
    product = db.query(Product).filter(Product.id == test_product).first()
    assert product.stock_quantity == 60  # 10 + 50
    db.close()


def test_create_purchase_empty_items(client, auth_token, test_supplier):
    """Test that creating a purchase with no items fails"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    purchase_data = {
        "supplier_id": test_supplier,
        "purchase_date": str(date.today()),
        "items": []
    }
    
    response = client.post("/api/v1/purchases/", json=purchase_data, headers=headers)
    
    # Should fail validation
    assert response.status_code == 422


def test_create_purchase_invalid_product(client, auth_token, test_supplier):
    """Test that creating a purchase with invalid product fails"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    purchase_data = {
        "supplier_id": test_supplier,
        "purchase_date": str(date.today()),
        "items": [
            {
                "product_id": 99999,  # Non-existent product
                "quantity": 10,
                "unit_price": "50.00"
            }
        ]
    }
    
    response = client.post("/api/v1/purchases/", json=purchase_data, headers=headers)
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_create_purchase_invalid_supplier(client, auth_token, test_product):
    """Test that creating a purchase with invalid supplier fails"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    purchase_data = {
        "supplier_id": 99999,  # Non-existent supplier
        "purchase_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 10,
                "unit_price": "50.00"
            }
        ]
    }
    
    response = client.post("/api/v1/purchases/", json=purchase_data, headers=headers)
    
    assert response.status_code == 404
    assert "supplier" in response.json()["detail"].lower()


def test_list_purchases(client, auth_token, test_supplier, test_product):
    """Test listing all purchases"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create a purchase first
    purchase_data = {
        "supplier_id": test_supplier,
        "purchase_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 20,
                "unit_price": "45.00"
            }
        ]
    }
    client.post("/api/v1/purchases/", json=purchase_data, headers=headers)
    
    # List purchases
    response = client.get("/api/v1/purchases/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_purchase_by_id(client, auth_token, test_supplier, test_product):
    """Test getting a single purchase by ID"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create a purchase
    purchase_data = {
        "supplier_id": test_supplier,
        "purchase_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 30,
                "unit_price": "45.00"
            }
        ]
    }
    create_response = client.post("/api/v1/purchases/", json=purchase_data, headers=headers)
    purchase_id = create_response.json()["id"]
    
    # Get the purchase
    response = client.get(f"/api/v1/purchases/{purchase_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == purchase_id
    assert len(data["items"]) == 1


def test_get_purchase_not_found(client, auth_token):
    """Test getting a non-existent purchase returns 404"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = client.get("/api/v1/purchases/99999", headers=headers)
    
    assert response.status_code == 404


def test_update_purchase(client, auth_token, test_supplier, test_product):
    """Test updating a purchase"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create initial purchase
    purchase_data = {
        "supplier_id": test_supplier,
        "purchase_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 50,
                "unit_price": "45.00"
            }
        ]
    }
    create_response = client.post("/api/v1/purchases/", json=purchase_data, headers=headers)
    purchase_id = create_response.json()["id"]
    
    # Check initial stock
    db = TestingSessionLocal()
    product = db.query(Product).filter(Product.id == test_product).first()
    stock_after_create = product.stock_quantity
    db.close()
    
    # Update purchase with different quantity
    update_data = {
        "items": [
            {
                "product_id": test_product,
                "quantity": 30,  # Changed from 50 to 30
                "unit_price": "45.00"
            }
        ]
    }
    response = client.put(f"/api/v1/purchases/{purchase_id}", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check updated calculations
    assert Decimal(str(data["subtotal"])) == Decimal("1350.00")  # 30 * 45
    assert Decimal(str(data["total"])) == Decimal("1350.00")
    
    # Verify stock was adjusted correctly
    # Should have removed 50 and then added 30, net change: -20
    db = TestingSessionLocal()
    product = db.query(Product).filter(Product.id == test_product).first()
    assert product.stock_quantity == stock_after_create - 20
    db.close()


def test_delete_purchase(client, auth_token, test_supplier, test_product):
    """Test deleting a purchase"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create a purchase
    purchase_data = {
        "supplier_id": test_supplier,
        "purchase_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 25,
                "unit_price": "45.00"
            }
        ]
    }
    create_response = client.post("/api/v1/purchases/", json=purchase_data, headers=headers)
    purchase_id = create_response.json()["id"]
    
    # Check stock after creation
    db = TestingSessionLocal()
    product = db.query(Product).filter(Product.id == test_product).first()
    stock_after_create = product.stock_quantity
    db.close()
    
    # Delete the purchase
    response = client.delete(f"/api/v1/purchases/{purchase_id}", headers=headers)
    
    assert response.status_code == 204
    
    # Verify purchase is deleted
    get_response = client.get(f"/api/v1/purchases/{purchase_id}", headers=headers)
    assert get_response.status_code == 404
    
    # Verify stock was reduced (removed the added stock)
    db = TestingSessionLocal()
    product = db.query(Product).filter(Product.id == test_product).first()
    assert product.stock_quantity == stock_after_create - 25  # Stock removed
    db.close()


def test_calculation_accuracy_multiple_items(client, auth_token, test_supplier, test_db):
    """Test that calculations are accurate with multiple items"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create multiple products
    db = TestingSessionLocal()
    product1 = Product(name="Product 1", sku="P1", price=Decimal("100.00"), cost=Decimal("40.00"), stock_quantity=10)
    product2 = Product(name="Product 2", sku="P2", price=Decimal("150.00"), cost=Decimal("62.50"), stock_quantity=10)
    db.add_all([product1, product2])
    db.commit()
    p1_id = product1.id
    p2_id = product2.id
    db.close()
    
    # Create purchase with multiple items
    purchase_data = {
        "supplier_id": test_supplier,
        "purchase_date": str(date.today()),
        "items": [
            {
                "product_id": p1_id,
                "quantity": 100,
                "unit_price": "40.00"
            },
            {
                "product_id": p2_id,
                "quantity": 50,
                "unit_price": "62.50"
            }
        ]
    }
    
    response = client.post("/api/v1/purchases/", json=purchase_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    
    # Check calculations (100*40 + 50*62.50 = 4000 + 3125 = 7125)
    assert Decimal(str(data["subtotal"])) == Decimal("7125.00")
    assert Decimal(str(data["total"])) == Decimal("7125.00")
    
    # Check individual item subtotals
    items = sorted(data["items"], key=lambda x: x["product_id"])
    assert Decimal(str(items[0]["subtotal"])) == Decimal("4000.00")  # 100 * 40
    assert Decimal(str(items[1]["subtotal"])) == Decimal("3125.00")  # 50 * 62.50


def test_purchase_number_auto_generation(client, auth_token, test_supplier, test_product):
    """Test that purchase numbers are auto-generated and incremented"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create first purchase
    purchase_data1 = {
        "supplier_id": test_supplier,
        "purchase_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 10,
                "unit_price": "45.00"
            }
        ]
    }
    response1 = client.post("/api/v1/purchases/", json=purchase_data1, headers=headers)
    purchase_num1 = response1.json()["purchase_number"]
    
    # Create second purchase
    purchase_data2 = {
        "supplier_id": test_supplier,
        "purchase_date": str(date.today()),
        "items": [
            {
                "product_id": test_product,
                "quantity": 15,
                "unit_price": "45.00"
            }
        ]
    }
    response2 = client.post("/api/v1/purchases/", json=purchase_data2, headers=headers)
    purchase_num2 = response2.json()["purchase_number"]
    
    # Verify numbers are sequential
    assert purchase_num1 is not None
    assert purchase_num2 is not None
    assert purchase_num1 != purchase_num2
    
    # Extract numbers and verify increment
    num1 = int(purchase_num1.split("-")[-1])
    num2 = int(purchase_num2.split("-")[-1])
    assert num2 == num1 + 1
