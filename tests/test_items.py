import pytest
from fastapi.testclient import TestClient
from app.main import app

# TestClient creates a fake HTTP client pointed at your FastAPI app
# No server needed — everything runs in memory
# AFTER — raise_server_exceptions=False lets your custom
# exception handlers fire exactly as they do in production
client = TestClient(app, raise_server_exceptions=False)


# ── Helper ─────────────────────────────────────────────────────────────────

def create_sample_item(name="Laptop", price=999.99):
    """Reusable helper — avoids repeating POST body in every test."""
    response = client.post("/items/", json={"name": name, "price": price})
    return response


# ── GET all items ───────────────────────────────────────────────────────────

def test_get_all_items_empty():
    """On a fresh app start, the list must be empty."""
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ── POST create item ────────────────────────────────────────────────────────

def test_create_item_success():
    """POST with valid body must return 201 and assign an id."""
    response = create_sample_item("Monitor", 299.99)
    data = response.json()

    assert response.status_code == 201
    assert data["name"] == "Monitor"
    assert data["price"] == 299.99
    assert data["in_stock"] is True        # default value
    assert "id" in data                    # server must assign id
    assert data["id"] is not None


def test_create_item_missing_required_field():
    """POST without 'price' (required field) must return 422 Validation Error."""
    response = client.post("/items/", json={"name": "Broken Item"})
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False        # our custom error shape


# ── GET by ID ───────────────────────────────────────────────────────────────

def test_get_item_by_id_success():
    """GET a specific item that exists must return 200 with correct data."""
    created = create_sample_item("Keyboard", 79.99).json()
    item_id = created["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Keyboard"


def test_get_item_not_found():
    """GET an item that doesn't exist must return 404 with our error shape."""
    response = client.get("/items/99999")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["status_code"] == 404


# ── PUT update item ─────────────────────────────────────────────────────────

def test_update_item_success():
    """PUT with valid id must return 200 with updated data."""
    created = create_sample_item("Old Mouse", 29.99).json()
    item_id = created["id"]

    response = client.put(
        f"/items/{item_id}",
        json={"name": "New Mouse", "price": 49.99, "in_stock": False}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "New Mouse"
    assert data["price"] == 49.99
    assert data["id"] == item_id           # id must not change


def test_update_item_not_found():
    """PUT on a missing id must return 404."""
    response = client.put(
        "/items/99999",
        json={"name": "Ghost", "price": 0.0}
    )
    assert response.status_code == 404


# ── DELETE item ─────────────────────────────────────────────────────────────

def test_delete_item_success():
    """DELETE an existing item must return 204 with no body."""
    created = create_sample_item("Headphones", 149.99).json()
    item_id = created["id"]

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204
    assert response.content == b""        # 204 = no body, ever

    # Confirm it is truly gone
    follow_up = client.get(f"/items/{item_id}")
    assert follow_up.status_code == 404


def test_delete_item_not_found():
    """DELETE on a missing id must return 404."""
    response = client.delete("/items/99999")
    assert response.status_code == 404


# ── Health check ────────────────────────────────────────────────────────────

def test_health_check():
    """Root endpoint must always return 200 with status ok."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
