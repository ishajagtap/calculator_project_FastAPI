"""Integration tests for the FastAPI Calculator API endpoints."""
import pytest
from fastapi.testclient import TestClient

from fastapi_app import app, calculation_history


@pytest.fixture(autouse=True)
def clear_history():
    """Reset in-memory history before every test."""
    calculation_history.clear()
    yield
    calculation_history.clear()


client = TestClient(app)


# ── /health ───────────────────────────────────────────────────────────────────

def test_health_check():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


# ── /operations ───────────────────────────────────────────────────────────────

def test_list_operations():
    resp = client.get("/operations")
    assert resp.status_code == 200
    ops = resp.json()["operations"]
    assert "add" in ops
    assert "div" in ops
    assert "mul" in ops


# ── GET / (home page) ─────────────────────────────────────────────────────────

def test_home_page_returns_html():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert b"FastAPI Calculator" in resp.content


# ── POST /calculate — success cases ───────────────────────────────────────────

@pytest.mark.parametrize("op,a,b,expected", [
    ("add",        10,   3,  13.0),
    ("sub",        10,   3,   7.0),
    ("mul",         4,   3,  12.0),
    ("div",        10,   2,   5.0),
    ("pow",         2,   8, 256.0),
    ("mod",        10,   3,   1.0),
    ("int_divide", 10,   3,   3.0),
    ("percent",    50, 200,  25.0),
    ("abs_diff",    3,  10,   7.0),
])
def test_calculate_operations(op, a, b, expected):
    resp = client.post("/calculate", data={"operation": op, "a": a, "b": b})
    assert resp.status_code == 200
    body = resp.json()
    assert "error" not in body
    assert abs(body["result"] - expected) < 1e-6


def test_calculate_root():
    resp = client.post("/calculate", data={"operation": "root", "a": 27, "b": 3})
    assert resp.status_code == 200
    assert abs(resp.json()["result"] - 3.0) < 1e-6


def test_calculate_returns_operands():
    resp = client.post("/calculate", data={"operation": "add", "a": 7, "b": 5})
    body = resp.json()
    assert body["a"] == 7.0
    assert body["b"] == 5.0
    assert body["operation"] == "add"


# ── POST /calculate — error cases ─────────────────────────────────────────────

def test_calculate_division_by_zero():
    resp = client.post("/calculate", data={"operation": "div", "a": 5, "b": 0})
    assert resp.status_code == 400
    assert "error" in resp.json()


def test_calculate_modulus_by_zero():
    resp = client.post("/calculate", data={"operation": "mod", "a": 5, "b": 0})
    assert resp.status_code == 400
    assert "error" in resp.json()


def test_calculate_int_divide_by_zero():
    resp = client.post("/calculate", data={"operation": "int_divide", "a": 5, "b": 0})
    assert resp.status_code == 400
    assert "error" in resp.json()


def test_calculate_percent_by_zero():
    resp = client.post("/calculate", data={"operation": "percent", "a": 50, "b": 0})
    assert resp.status_code == 400
    assert "error" in resp.json()


def test_calculate_unknown_operation():
    resp = client.post("/calculate", data={"operation": "foobar", "a": 1, "b": 2})
    assert resp.status_code == 400
    assert "error" in resp.json()


def test_calculate_root_even_negative():
    resp = client.post("/calculate", data={"operation": "root", "a": -4, "b": 2})
    assert resp.status_code == 400
    assert "error" in resp.json()


# ── GET /history ──────────────────────────────────────────────────────────────

def test_history_initially_empty():
    resp = client.get("/history")
    assert resp.status_code == 200
    assert resp.json()["history"] == []


def test_history_records_calculation():
    client.post("/calculate", data={"operation": "add", "a": 2, "b": 3})
    resp = client.get("/history")
    history = resp.json()["history"]
    assert len(history) == 1
    assert history[0]["operation"] == "add"
    assert history[0]["result"] == 5.0


def test_history_accumulates():
    client.post("/calculate", data={"operation": "add", "a": 1, "b": 1})
    client.post("/calculate", data={"operation": "mul", "a": 3, "b": 4})
    resp = client.get("/history")
    assert len(resp.json()["history"]) == 2


def test_history_not_updated_on_error():
    client.post("/calculate", data={"operation": "div", "a": 1, "b": 0})
    resp = client.get("/history")
    assert resp.json()["history"] == []


# ── DELETE /history ───────────────────────────────────────────────────────────

def test_delete_history():
    client.post("/calculate", data={"operation": "add", "a": 1, "b": 2})
    resp = client.delete("/history")
    assert resp.status_code == 200
    assert resp.json()["message"] == "History cleared"
    assert client.get("/history").json()["history"] == []
