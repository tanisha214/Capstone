"""
Login Tests — PyTest
Tests for the Login functionality of TutorialsNinja Demo
Uses PyTest fixtures, markers, parametrize, and POM
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from utilities.logger import get_logger
from utilities.csv_reader import CSVReader
from tests.conftest import get_login_params

logger = get_logger(__name__)

# ─────────────────── Load valid creds from CSV ───────────────────
_LOGIN_CSV = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "test_data", "login_data.csv"
)
_ALL_ROWS      = CSVReader.read_csv(_LOGIN_CSV)
_VALID_CREDS   = next((r for r in _ALL_ROWS if r.get("expected_result","").lower() == "success"), None)
_VALID_EMAIL   = _VALID_CREDS["email"]    if _VALID_CREDS else "no_valid@test.com"
_VALID_PASS    = _VALID_CREDS["password"] if _VALID_CREDS else "NoPass"

# Parametrized data
LOGIN_PARAMS = get_login_params()


# ═══════════════════════════════════════════════════════════════
# TEST CLASS
# ═══════════════════════════════════════════════════════════════

@pytest.mark.login
class TestLoginPytest:
    """PyTest-based Login Test Suite using fixtures and POM"""

    # ──────────────────── TC_PY_LOGIN_001 ─────────────────────
    @pytest.mark.smoke
    def test_TC_PY_LOGIN_001_login_page_loads(self, driver):
        """TC_PY_LOGIN_001: Login page loads with correct title"""
        logger.info("TC_PY_LOGIN_001: Login Page Load Test")

        home = HomePage(driver)
        home.navigate_to_login()

        login_page = LoginPage(driver)
        title = login_page.get_title()

        assert "Account Login" in title, f"Expected 'Account Login' in title, got: {title}"
        logger.info("TC_PY_LOGIN_001 PASSED ✓")

    # ──────────────────── TC_PY_LOGIN_002 ───────────────────
    @pytest.mark.smoke
    def test_TC_PY_LOGIN_002_valid_login_redirects_to_account(self, driver):
        """TC_PY_LOGIN_002: Valid credentials redirect to account dashboard"""
        logger.info("TC_PY_LOGIN_002: Valid Login Redirect Test")
        logger.info(f"Using credentials from CSV: {_VALID_EMAIL}")

        home = HomePage(driver)
        home.navigate_to_login()

        login_page = LoginPage(driver)
        login_page.login(_VALID_EMAIL, _VALID_PASS)

        account = AccountPage(driver)
        assert account.is_logged_in(), \
            f"User should be on account page after valid login ({_VALID_EMAIL})"
        logger.info("TC_PY_LOGIN_002 PASSED ✓")

    # ──────────────────── TC_PY_LOGIN_003 ─────────────────────
    @pytest.mark.negative
    def test_TC_PY_LOGIN_003_invalid_login_shows_error(self, driver):
        """TC_PY_LOGIN_003: Invalid credentials display error alert"""
        logger.info("TC_PY_LOGIN_003: Invalid Login Error Test")

        home = HomePage(driver)
        home.navigate_to_login()

        login_page = LoginPage(driver)
        login_page.login("bad@email.com", "BadPass999")

        assert login_page.is_login_error_displayed(), \
            "Error alert should be visible for invalid login"
        logger.info("TC_PY_LOGIN_003 PASSED ✓")

    # ──────────────────── TC_PY_LOGIN_004 ─────────────────────
    @pytest.mark.negative
    def test_TC_PY_LOGIN_004_error_message_content(self, driver):
        """TC_PY_LOGIN_004: Error message contains expected warning text"""
        logger.info("TC_PY_LOGIN_004: Error Message Content Test")

        home = HomePage(driver)
        home.navigate_to_login()

        login_page = LoginPage(driver)
        login_page.login("wrong@user.com", "WrongPwd")

        error_msg = login_page.get_error_message()
        logger.info(f"Error message received: {error_msg}")

        assert len(error_msg) > 0, "Error message should not be empty"
        assert any(keyword in error_msg.lower() for keyword in
                   ["warning", "match", "no match", "incorrect", "invalid"]), \
            f"Unexpected error message: '{error_msg}'"
        logger.info("TC_PY_LOGIN_004 PASSED ✓")

    # ──────────────────── TC_PY_LOGIN_005 ─────────────────────
    @pytest.mark.negative
    def test_TC_PY_LOGIN_005_empty_credentials(self, driver):
        """TC_PY_LOGIN_005: Empty credentials trigger validation error"""
        logger.info("TC_PY_LOGIN_005: Empty Credentials Test")

        home = HomePage(driver)
        home.navigate_to_login()

        login_page = LoginPage(driver)
        login_page.login("", "")

        assert login_page.is_login_error_displayed(), \
            "Error should be displayed when both fields are empty"
        logger.info("TC_PY_LOGIN_005 PASSED ✓")

    # ──────────────────── TC_PY_LOGIN_006 ─────────────────────
    def test_TC_PY_LOGIN_006_returning_customer_heading(self, driver):
        """TC_PY_LOGIN_006: Login page shows 'Returning Customer' heading"""
        logger.info("TC_PY_LOGIN_006: Returning Customer Heading Test")

        home = HomePage(driver)
        home.navigate_to_login()

        login_page = LoginPage(driver)
        heading = login_page.get_page_heading()

        assert "Returning Customer" in heading, \
            f"Expected 'Returning Customer' in heading, got: '{heading}'"
        logger.info("TC_PY_LOGIN_006 PASSED ✓")

    # ──────────────────── TC_PY_LOGIN_007 ─────────────────────
    def test_TC_PY_LOGIN_007_forgotten_password_navigation(self, driver):
        """TC_PY_LOGIN_007: Forgotten Password link navigates to correct page"""
        logger.info("TC_PY_LOGIN_007: Forgotten Password Navigation Test")

        home = HomePage(driver)
        home.navigate_to_login()

        login_page = LoginPage(driver)
        login_page.click_forgotten_password()

        assert "forgotten" in driver.current_url.lower(), \
            "Should navigate to forgotten password page"
        logger.info("TC_PY_LOGIN_007 PASSED ✓")

    # ──────────────────── TC_PY_LOGIN_008 (Parametrized) ──────
    @pytest.mark.parametrize(
        "email, password, expected",
        LOGIN_PARAMS if LOGIN_PARAMS else [
            ("test@example.com", "Test@1234", "success"),
            ("invalid@user.com", "wrongpassword", "failure"),
        ]
    )
    @pytest.mark.regression
    def test_TC_PY_LOGIN_008_parametrized_login(self, driver, email, password, expected):
        """TC_PY_LOGIN_008: Data-driven login test using CSV via @pytest.mark.parametrize"""
        logger.info(f"TC_PY_LOGIN_008: Testing login: {email} | expected: {expected}")

        home = HomePage(driver)
        home.navigate_to_login()

        login_page = LoginPage(driver)
        login_page.login(email, password)

        if expected.lower() == "success":
            account = AccountPage(driver)
            assert account.is_logged_in(), \
                f"Expected successful login for: {email}"
        else:
            assert login_page.is_login_error_displayed(), \
                f"Expected login failure for: {email}"

        logger.info(f"TC_PY_LOGIN_008 PASSED ✓ | {email} | {expected}")
