"""
Login Tests — Unittest
Tests for the Login functionality of TutorialsNinja Demo
Uses Page Object Model (POM) and data from CSV
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.unittest_tests.base_test import BaseTest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from utilities.csv_reader import CSVReader
from utilities.logger import get_logger

logger = get_logger(__name__)

# ───────────────────── Load CSV Test Data ─────────────────────
LOGIN_CSV = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "test_data", "login_data.csv"
)

# Read valid and invalid credentials once at module load
_ALL_ROWS       = CSVReader.read_csv(LOGIN_CSV)
_VALID_CREDS    = next((r for r in _ALL_ROWS if r.get("expected_result","").lower() == "success"), None)
_INVALID_CREDS  = next((r for r in _ALL_ROWS if r.get("expected_result","").lower() == "failure"), None)

# Convenience vars (fall back to obvious-fail values if CSV is empty)
_VALID_EMAIL    = _VALID_CREDS["email"]    if _VALID_CREDS    else "no_valid_user@test.com"
_VALID_PASS     = _VALID_CREDS["password"] if _VALID_CREDS    else "NoValidPass"
_INVALID_EMAIL  = _INVALID_CREDS["email"]  if _INVALID_CREDS  else "invalid@test.com"
_INVALID_PASS   = _INVALID_CREDS["password"] if _INVALID_CREDS else "WrongPass"



class TestLoginFunctionality(BaseTest):
    """
    Unittest Test Suite for Login Functionality.
    Tests valid login, invalid login, empty fields, navigation.
    """

    # ──────────────────── TC_LOGIN_001 ────────────────────────
    def test_TC_LOGIN_001_valid_login(self):
        """TC_LOGIN_001: Login with valid credentials navigates to account page"""
        logger.info("TC_LOGIN_001: Valid Login Test")
        logger.info(f"Using credentials from CSV: {_VALID_EMAIL}")

        home = HomePage(self.driver)
        home.navigate_to_login()

        login_page = LoginPage(self.driver)
        self.assertIn("Login", login_page.get_title(),
                      "Login page title should contain 'Login'")

        login_page.login(_VALID_EMAIL, _VALID_PASS)

        account = AccountPage(self.driver)
        self.assertTrue(
            account.is_logged_in(),
            f"User should be redirected to Account page after valid login ({_VALID_EMAIL})"
        )
        logger.info("TC_LOGIN_001 PASSED ✓")


    # ──────────────────── TC_LOGIN_002 ────────────────────────
    def test_TC_LOGIN_002_invalid_credentials(self):
        """TC_LOGIN_002: Login with invalid credentials shows error alert"""
        logger.info("TC_LOGIN_002: Invalid Credentials Test")

        home = HomePage(self.driver)
        home.navigate_to_login()

        login_page = LoginPage(self.driver)
        login_page.login(_INVALID_EMAIL, _INVALID_PASS)

        self.assertTrue(
            login_page.is_login_error_displayed(),
            "Error alert should be displayed for invalid credentials"
        )
        error_msg = login_page.get_error_message()
        logger.info(f"Error message: {error_msg}")
        self.assertGreater(len(error_msg), 0, "Error message should not be empty")
        logger.info("TC_LOGIN_002 PASSED ✓")


    # ──────────────────── TC_LOGIN_003 ────────────────────────
    def test_TC_LOGIN_003_empty_email_field(self):
        """TC_LOGIN_003: Login with empty email shows validation error"""
        logger.info("TC_LOGIN_003: Empty Email Validation Test")

        home = HomePage(self.driver)
        home.navigate_to_login()

        login_page = LoginPage(self.driver)
        login_page.login("", "SomePassword1")

        self.assertTrue(
            login_page.is_login_error_displayed(),
            "Error should appear when email is empty"
        )
        logger.info("TC_LOGIN_003 PASSED ✓")

    # ──────────────────── TC_LOGIN_004 ────────────────────────
    def test_TC_LOGIN_004_empty_password_field(self):
        """TC_LOGIN_004: Login with empty password shows validation error"""
        logger.info("TC_LOGIN_004: Empty Password Validation Test")

        home = HomePage(self.driver)
        home.navigate_to_login()

        login_page = LoginPage(self.driver)
        login_page.login("test@example.com", "")

        self.assertTrue(
            login_page.is_login_error_displayed(),
            "Error should appear when password is empty"
        )
        logger.info("TC_LOGIN_004 PASSED ✓")

    # ──────────────────── TC_LOGIN_005 ────────────────────────
    def test_TC_LOGIN_005_login_page_title(self):
        """TC_LOGIN_005: Login page has correct title"""
        logger.info("TC_LOGIN_005: Login Page Title Test")

        home = HomePage(self.driver)
        home.navigate_to_login()

        login_page = LoginPage(self.driver)
        title = login_page.get_title()

        self.assertIn("Account Login", title,
                      f"Expected 'Account Login' in title, got: '{title}'")
        logger.info("TC_LOGIN_005 PASSED ✓")

    # ──────────────────── TC_LOGIN_006 ────────────────────────
    def test_TC_LOGIN_006_login_page_heading(self):
        """TC_LOGIN_006: Login page displays 'Returning Customer' heading"""
        logger.info("TC_LOGIN_006: Login Page Heading Test")

        home = HomePage(self.driver)
        home.navigate_to_login()

        login_page = LoginPage(self.driver)
        heading = login_page.get_page_heading()
        logger.info(f"Page heading: '{heading}'")

        self.assertIn("Returning Customer", heading,
                      f"Expected 'Returning Customer' heading, got: '{heading}'")
        logger.info("TC_LOGIN_006 PASSED ✓")

    # ──────────────────── TC_LOGIN_007 ────────────────────────
    def test_TC_LOGIN_007_forgotten_password_link(self):
        """TC_LOGIN_007: Forgotten Password link navigates correctly"""
        logger.info("TC_LOGIN_007: Forgotten Password Navigation Test")

        home = HomePage(self.driver)
        home.navigate_to_login()

        login_page = LoginPage(self.driver)
        login_page.click_forgotten_password()

        self.assertIn("forgotten", self.driver.current_url.lower(),
                      "Should navigate to forgotten password page")
        logger.info("TC_LOGIN_007 PASSED ✓")

    # ──────────────────── TC_LOGIN_008 (Data-Driven) ──────────
    def test_TC_LOGIN_008_data_driven_login(self):
        """TC_LOGIN_008: Data-driven login tests from CSV (first row only in unittest)"""
        logger.info("TC_LOGIN_008: Data-Driven Login Test (CSV)")

        rows = CSVReader.read_csv(LOGIN_CSV)
        if not rows:
            self.skipTest("No login test data found in CSV")

        # Test first row of CSV
        row = rows[0]
        email = row.get("email", "")
        password = row.get("password", "")
        expected = row.get("expected_result", "").lower()

        logger.info(f"Testing: {email} | expected: {expected}")

        home = HomePage(self.driver)
        home.navigate_to_login()

        login_page = LoginPage(self.driver)
        login_page.login(email, password)

        if expected == "success":
            account = AccountPage(self.driver)
            self.assertTrue(account.is_logged_in(),
                            f"Expected successful login for {email}")
        else:
            self.assertTrue(login_page.is_login_error_displayed(),
                            f"Expected login failure for {email}")

        logger.info("TC_LOGIN_008 PASSED ✓")


# ─────────────────────── Run Tests ────────────────────────────
if __name__ == "__main__":
    unittest.main(verbosity=2)
