"""
Assignment 3: Dynamic Dropdowns & Checkboxes
Select checkboxes and verify with .is_selected(); type into an autocomplete
field and loop through suggestions to select a matching option.
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
    driver.get("https://rahulshettyacademy.com/AutomationPractice/")
    driver.maximize_window()

    # ---------- PART 1: Checkboxes ----------
    checkbox_values = ["option1", "option2", "option3"]

    for value in checkbox_values:
        checkbox = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//input[@value='{value}']"))
        )
        checkbox.click()

        # Verify state using .is_selected()
        is_checked = checkbox.is_selected()
        print(f"Checkbox '{value}' selected: {is_checked}")
        assert is_checked, f"Checkbox {value} was not selected!"

    print("PASS: All checkboxes selected and verified.\n")
    time.sleep(1)

    # ---------- PART 2: Autocomplete Dropdown ----------
    autocomplete_field = wait.until(
        EC.presence_of_element_located((By.ID, "autocomplete"))
    )
    autocomplete_field.send_keys("Ind")

    suggestions = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ui-menu-item div"))
    )

    print(f"Found {len(suggestions)} suggestions:")
    target_found = False
    for suggestion in suggestions:
        suggestion_text = suggestion.text.strip()   # capture text BEFORE clicking
        print(f"  - {suggestion_text}")

        if suggestion_text == "India":              # EXACT match, not substring
            print(f"PASS: Match found -> '{suggestion_text}'")
            suggestion.click()                       # click AFTER capturing text
            target_found = True
            break

    if not target_found:
        print("WARNING: No suggestion exactly matched 'India'")

    time.sleep(2)   # pause here regardless of match/no-match, so the result is visible

except Exception as e:
    print(f"ERROR: {e}")
finally:
    driver.quit()