"""
Assignment 7: Page Object Model

Tests login functionality using the LoginPage and
InventoryPage Page Objects.

Assertions are kept in this test file.
"""

import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestLogin:

    # -----------------------------------------------------
    # Valid Login
    # -----------------------------------------------------

    def test_valid_login(self, driver):

        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        login_page.login(
            "standard_user",
            "secret_sauce"
        )

        assert inventory_page.is_inventory_page_displayed()

        assert driver.current_url.endswith(
            "/inventory.html"
        )

    # -----------------------------------------------------
    # Invalid Password
    # -----------------------------------------------------

    def test_invalid_password(self, driver):

        login_page = LoginPage(driver)

        login_page.login(
            "standard_user",
            "wrong_password"
        )

        error_message = login_page.get_error_message()

        assert "Username and password" in error_message

    # -----------------------------------------------------
    # Locked Out User
    # -----------------------------------------------------

    def test_locked_out_user(self, driver):

        login_page = LoginPage(driver)

        login_page.login(
            "locked_out_user",
            "secret_sauce"
        )

        error_message = login_page.get_error_message()

        assert "locked out" in error_message.lower()