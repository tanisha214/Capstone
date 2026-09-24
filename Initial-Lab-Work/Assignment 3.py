"""
Assignment: CSS Selector Challenge - Wildcard Attribute Selectors
Target Environment: Arch Linux, Mozilla Firefox, GeckoDriver
Site: https://rahulshettyacademy.com/AutomationPractice/

Locators demonstrated:
  - Starts-with prefix:      [attribute^='value']
  - Contains substring:      [attribute*='value']
  - Ends-with suffix:        [attribute$='value']
"""

import sys
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

print("[BOOT] Launching CSS Selector Wildcard Challenge script...", flush=True)

URL = "https://rahulshettyacademy.com/AutomationPractice/"

def configure_firefox_driver(headless: bool = False) -> webdriver.Firefox:
    """
    Initializes Mozilla Firefox with GeckoDriver on Arch Linux.
    Resolves the system geckodriver binary or falls back to Selenium Manager.
    """
    options = FirefoxOptions()
    if headless:
        options.add_argument("-headless")

    options.add_argument("--width=1366")
    options.add_argument("--height=768")

    # Arch Linux default path: /usr/bin/geckodriver
    geckodriver_bin = shutil.which("geckodriver") or "/usr/bin/geckodriver"

    try:
        service = FirefoxService(executable_path=geckodriver_bin)
        driver = webdriver.Firefox(service=service, options=options)
    except WebDriverException:
        print("[INFO] Fallback: Engaging Selenium Manager for GeckoDriver...", flush=True)
        driver = webdriver.Firefox(options=options)

    driver.maximize_window()
    return driver

def main():
    driver = None
    try:
        print("=" * 75, flush=True)
        print("STARTING CSS WILDCARD ATTRIBUTE SELECTOR DEMO", flush=True)
        print("=" * 75, flush=True)

        driver = configure_firefox_driver(headless=False)
        wait = WebDriverWait(driver, 10)

        print(f"[*] Navigating to: {URL}", flush=True)
        driver.get(URL)

        # Wait until the page heading or practice container is ready
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        print("[✓] Page loaded successfully.\n", flush=True)

        print("-" * 75, flush=True)
        print("1. STARTS-WITH SELECTOR: [id^='checkBoxOption']", flush=True)
        print("-" * 75, flush=True)

        checkboxes = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "[id^='checkBoxOption']")
            )
        )
        print(f"[✓] Found {len(checkboxes)} checkboxes matching prefix [id^='checkBoxOption']", flush=True)
        for idx, cb in enumerate(checkboxes, start=1):
            cb_id = cb.get_attribute("id")
            cb.click()
            is_checked = cb.is_selected()
            print(f"    -> Checkbox #{idx} (id='{cb_id}') clicked | checked={is_checked}", flush=True)

        print("\n" + "-" * 75, flush=True)
        print("2. CONTAINS SELECTOR: [id*='BoxOption']", flush=True)
        print("-" * 75, flush=True)

        contains_match = driver.find_elements(By.CSS_SELECTOR, "[id*='BoxOption']")
        print(f"[✓] Found {len(contains_match)} elements containing substring 'BoxOption':", flush=True)
        for elem in contains_match:
            print(f"    -> Tag: <{elem.tag_name}> | id: '{elem.get_attribute('id')}'", flush=True)

        print("\n" + "-" * 75, flush=True)
        print("3. ENDS-WITH SELECTOR: [id$='Option3']", flush=True)
        print("-" * 75, flush=True)

        ends_with_match = driver.find_element(By.CSS_SELECTOR, "[id$='Option3']")
        print(f"[✓] Successfully matched ends-with element: id='{ends_with_match.get_attribute('id')}'", flush=True)

        print("\n" + "-" * 75, flush=True)
        print("4. RADIO BUTTON SELECTOR: [name^='radioButton']", flush=True)
        print("-" * 75, flush=True)

        radio_buttons = driver.find_elements(By.CSS_SELECTOR, "[name^='radioButton']")
        print(f"[✓] Found {len(radio_buttons)} radio buttons via [name^='radioButton']", flush=True)
        if radio_buttons:
            first_radio = radio_buttons[0]
            first_radio.click()
            print(f"    -> Clicked first radio button (value='{first_radio.get_attribute('value')}')", flush=True)
            print(f"    -> Selected status: {first_radio.is_selected()}", flush=True)

        # Brief pause to view browser actions before exit
        time.sleep(2)
        print("\n[SUCCESS] All wildcard selector operations completed successfully!", flush=True)

    except TimeoutException:
        print("[ERROR] Timed out waiting for page elements.", file=sys.stderr, flush=True)
    except WebDriverException as wde:
        print(f"[ERROR] Selenium WebDriver failure: {wde.msg}", file=sys.stderr, flush=True)
    finally:
        if driver:
            print("\n[*] Closing Firefox session...", flush=True)
            driver.quit()
            print("[✓] Session terminated cleanly.", flush=True)

if __name__ == "__main__":
    main()