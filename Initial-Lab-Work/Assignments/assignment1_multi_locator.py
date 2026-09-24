"""
Assignment 1: The Multi-Locator Challenge
Navigate to SauceDemo login page, interact using three different locator
strategies (ID, NAME, XPATH), and validate successful login via URL check.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    time.sleep(2)
    # Locator Strategy 1: By.ID
    username_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    username_field.send_keys("standard_user")

    # Locator Strategy 2: By.NAME
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("secret_sauce")
    time.sleep(2)
    # Locator Strategy 3: By.XPATH
    login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
    login_button.click()

    wait.until(EC.url_contains("/inventory.html"))
    current_url = driver.current_url

    assert "/inventory.html" in current_url, f"Login failed! Current URL: {current_url}"
    print(f"PASS: Login successful. Current URL: {current_url}")

    time.sleep(2)

except AssertionError as e:
    print(f"TEST FAILED: {e}")
except Exception as e:
    print(f"ERROR: {e}")
finally:
    driver.quit()
