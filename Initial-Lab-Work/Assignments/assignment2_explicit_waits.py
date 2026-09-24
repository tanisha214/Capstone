"""
Assignment 2: Synchronization & Explicit Waits
Uses demo.guru99.com/test/ajax.html - a page purpose-built for teaching
this exact wait pattern. Clicking a radio button + Check button triggers
an AJAX call that updates a text element after a short server delay.

NO time.sleep() is used anywhere. All waits are WebDriverWait +
expected_conditions, as the assignment requires.
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
    driver.get("https://demo.guru99.com/test/ajax.html")
    driver.maximize_window()

    # Wait for the page's main container to be present before doing anything
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".container")))

    # Capture the text BEFORE the AJAX call happens (for comparison)
    text_element = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "radiobutton"))
    )
    text_before = text_element.text.strip()
    print(f"Text BEFORE AJAX call: '{text_before}'")
    time.sleep(2)
    # Click the "Yes" radio button
    yes_radio = wait.until(EC.element_to_be_clickable((By.ID, "yes")))
    yes_radio.click()
    time.sleep(2)
    # Click the "Check" button - this triggers the actual AJAX request
    check_button = wait.until(EC.element_to_be_clickable((By.ID, "buttoncheck")))
    check_button.click()

    wait.until(lambda d: d.find_element(By.CLASS_NAME, "radiobutton").text.strip() != text_before)

    text_after = driver.find_element(By.CLASS_NAME, "radiobutton").text.strip()
    print(f"Text AFTER AJAX call: '{text_after}'")

    expected_text = "Radio button is checked and it's value is Yes"

    assert text_after != text_before, "AJAX call did not update the text!"
    assert text_after == expected_text, (
        f"Text mismatch! Expected: '{expected_text}', Got: '{text_after}'"
    )

    print(f"PASS: AJAX content updated correctly -> '{text_after}'")

except AssertionError as e:
    print(f"TEST FAILED: {e}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
finally:
    driver.quit()