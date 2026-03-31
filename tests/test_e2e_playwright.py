"""End-to-end tests using Playwright — simulates real browser interactions."""
import pytest
from playwright.sync_api import Page, expect


# All E2E tests receive `live_server_url` from root conftest.py
# and `page` from pytest-playwright.

def _go(page: Page, url: str) -> None:
    """Navigate and wait for the page to fully load."""
    page.goto(url)
    page.wait_for_load_state("networkidle")


def _calculate(page: Page, operation: str, a: str, b: str) -> None:
    """Fill the calculator form and submit."""
    page.select_option("#operation", operation)
    page.fill("#a", a)
    page.fill("#b", b)
    page.click("#calculate-btn")
    # Wait for the result box to become visible
    page.wait_for_selector("#result-box", state="visible")


# ── Basic page load ────────────────────────────────────────────────────────────

def test_page_title(page: Page, live_server_url: str):
    _go(page, live_server_url)
    expect(page).to_have_title("FastAPI Calculator")


def test_page_has_calculate_button(page: Page, live_server_url: str):
    _go(page, live_server_url)
    expect(page.locator("#calculate-btn")).to_be_visible()


def test_page_has_operation_select(page: Page, live_server_url: str):
    _go(page, live_server_url)
    expect(page.locator("#operation")).to_be_visible()


# ── Arithmetic operations ──────────────────────────────────────────────────────

def test_add(page: Page, live_server_url: str):
    _go(page, live_server_url)
    _calculate(page, "add", "5", "3")
    result_text = page.locator("#result").inner_text()
    assert "8" in result_text


def test_subtract(page: Page, live_server_url: str):
    _go(page, live_server_url)
    _calculate(page, "sub", "10", "4")
    result_text = page.locator("#result").inner_text()
    assert "6" in result_text


def test_multiply(page: Page, live_server_url: str):
    _go(page, live_server_url)
    _calculate(page, "mul", "6", "7")
    result_text = page.locator("#result").inner_text()
    assert "42" in result_text


def test_divide(page: Page, live_server_url: str):
    _go(page, live_server_url)
    _calculate(page, "div", "20", "4")
    result_text = page.locator("#result").inner_text()
    assert "5" in result_text


def test_power(page: Page, live_server_url: str):
    _go(page, live_server_url)
    _calculate(page, "pow", "2", "10")
    result_text = page.locator("#result").inner_text()
    assert "1024" in result_text


def test_modulus(page: Page, live_server_url: str):
    _go(page, live_server_url)
    _calculate(page, "mod", "10", "3")
    result_text = page.locator("#result").inner_text()
    assert "1" in result_text


def test_abs_diff(page: Page, live_server_url: str):
    _go(page, live_server_url)
    _calculate(page, "abs_diff", "3", "10")
    result_text = page.locator("#result").inner_text()
    assert "7" in result_text


# ── Error handling ────────────────────────────────────────────────────────────

def test_division_by_zero_shows_error(page: Page, live_server_url: str):
    _go(page, live_server_url)
    _calculate(page, "div", "9", "0")
    result_box = page.locator("#result-box")
    expect(result_box).to_have_class("error")
    assert "Error" in page.locator("#result").inner_text()


# ── History updates in UI ─────────────────────────────────────────────────────

def test_history_table_appears_after_calculation(page: Page, live_server_url: str):
    _go(page, live_server_url)
    _calculate(page, "add", "1", "2")
    # History table should now be visible
    expect(page.locator("#history-table")).to_be_visible()


def test_history_table_shows_result(page: Page, live_server_url: str):
    _go(page, live_server_url)
    _calculate(page, "mul", "3", "4")
    rows = page.locator("#history-body tr")
    expect(rows).to_have_count(1)
    row_text = rows.first.inner_text()
    assert "12" in row_text
