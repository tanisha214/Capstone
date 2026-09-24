"""
Assignment 9: PyTest Integration with HTML Reporting
Test suite that uses the `driver` fixture from conftest.py.
Run from terminal with:
    pytest test_login_suite.py --html=report.html --self-contained-html
"""

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_valid_login(driver):
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_loaded(), "Dashboard should load after valid login"
    assert dashboard_page.get_item_count() > 0, "Inventory should show items"


def test_invalid_password_shows_error(driver):
    login_page = LoginPage(driver)
    login_page.login("standard_user", "wrong_password")

    error_text = login_page.get_error_message()
    assert error_text is not None, "Error message should appear"
    assert "do not match" in error_text.lower() or "username and password" in error_text.lower()


def test_locked_out_user_is_blocked(driver):
    login_page = LoginPage(driver)
    login_page.login("locked_out_user", "secret_sauce")

    error_text = login_page.get_error_message()
    assert error_text is not None, "Locked-out user should see an error"
    assert "locked out" in error_text.lower()


def test_intentional_failure_for_demo(driver):
    """
    This test is intentionally wrong to demonstrate the HTML report
    capturing a FAILED test with an embedded screenshot.
    """
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")

    dashboard_page = DashboardPage(driver)
    # Deliberately wrong assertion to show failure + screenshot in report
    assert dashboard_page.get_item_count() == 999, "Intentional failure for demo"
