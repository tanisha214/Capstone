"""
Assignment 7: Page Object Model (POM) Restructure
This test file contains ONLY assertions and test flow.
All locators and UI actions live inside the Page Object classes.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()

try:
    # ---------- Test Case 1: Valid Login ----------
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_loaded(), "Dashboard did not load after valid login!"
    print(f"✅ PASS: Logged in. Page title: '{dashboard_page.get_page_title_text()}'")
    print(f"   Inventory items found: {dashboard_page.get_item_count()}")

    dashboard_page.logout()
    print("✅ PASS: Logged out successfully.\n")

    # ---------- Test Case 2: Invalid Login ----------
    login_page2 = LoginPage(driver)
    login_page2.login("standard_user", "wrong_password")

    error_text = login_page2.get_error_message()
    assert error_text is not None, "Expected an error message but none appeared!"
    print(f"✅ PASS: Correct error shown for invalid login -> '{error_text}'")

except AssertionError as e:
    print(f"❌ TEST FAILED: {e}")
finally:
    driver.quit()
