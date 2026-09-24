"""
Assignment 2: Child Nodes Using CSS - CSS child/descendant selectors
Target Environment: Arch Linux, Mozilla Firefox, GeckoDriver
Sites:
  - Part A: https://rahulshettyacademy.com/AutomationPractice/
  - Part B: https://testautomationpractice.blogspot.com/
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

print("[BOOT] Initializing Assignment 2 (Child Nodes CSS Selectors)...", flush=True)

def configure_firefox_driver(headless: bool = False) -> webdriver.Firefox:
    """
    Configures and initializes Mozilla Firefox using GeckoDriver on Arch Linux.
    Resolves /usr/bin/geckodriver directly with automatic Selenium Manager fallback.
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

def part_a_direct_child_checkbox():
    """
    Part A: Targets direct child elements using the '>' combinator.
    Demonstrates locating labels and child checkbox inputs on Rahul Shetty Academy.
    """
    target_url = "https://rahulshettyacademy.com/AutomationPractice/"
    driver = None

    print("\n" + "=" * 75, flush=True)
    print("STARTING PART A: DIRECT CHILD SELECTORS ('fieldset > label')", flush=True)
    print("=" * 75, flush=True)

    try:
        driver = configure_firefox_driver(headless=False)
        wait = WebDriverWait(driver, 10)

        print(f"[*] Navigating to: {target_url}", flush=True)
        driver.get(target_url)

        # Wait until fieldset labels are present in the DOM
        labels = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "fieldset > label"))
        )
        print(f"[✓] Found {len(labels)} labels via 'fieldset > label'", flush=True)

        # Locate direct child checkbox inputs
        checkboxes = driver.find_elements(
            By.CSS_SELECTOR, "fieldset > label > input[type='checkbox']"
        )
        print(f"[✓] Found {len(checkboxes)} checkboxes via 'fieldset > label > input[type=\"checkbox\"]'", flush=True)

        for idx, cb in enumerate(checkboxes, start=1):
            cb_id = cb.get_attribute("id") or f"unnamed-index-{idx}"
            cb.click()
            is_checked = cb.is_selected()
            print(f"    -> Clicked Checkbox #{idx} (id='{cb_id}') | checked={is_checked}", flush=True)

        time.sleep(2)
        print("[✓] Part A completed successfully.", flush=True)

    except TimeoutException:
        print("[ERROR] Part A timed out waiting for DOM elements.", file=sys.stderr, flush=True)
    except WebDriverException as wde:
        print(f"[ERROR] Part A WebDriver failure: {wde.msg}", file=sys.stderr, flush=True)
    finally:
        if driver:
            print("[*] Closing Part A browser session...", flush=True)
            driver.quit()
            print("[✓] Session terminated cleanly.", flush=True)

def part_b_table_child_selector():
    """
    Part B: Uses direct descendant selectors to navigate table rows and columns.
    Demonstrates extracting specific row/column cells and iterating over column data.
    """
    target_url = "https://testautomationpractice.blogspot.com/"
    driver = None

    print("\n" + "=" * 75, flush=True)
    print("STARTING PART B: TABLE CHILD SELECTORS ('table#productTable > tbody > tr')", flush=True)
    print("=" * 75, flush=True)

    try:
        driver = configure_firefox_driver(headless=False)
        wait = WebDriverWait(driver, 10)

        print(f"[*] Navigating to: {target_url}", flush=True)
        driver.get(target_url)

        # Wait until the target table rows are present in the DOM
        rows = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "table#productTable > tbody > tr")
            )
        )
        print(f"[✓] Found {len(rows)} data rows via 'table#productTable > tbody > tr'", flush=True)

        # Extract cell from the first row, first column
        first_id_cell = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table#productTable > tbody > tr:nth-child(1) > td:nth-child(1)")
            )
        )
        print(f"[✓] First row, first column text: '{first_id_cell.text.strip()}'", flush=True)

        # Extract all product names (column 2 across all table body rows)
        product_cells = driver.find_elements(
            By.CSS_SELECTOR, "table#productTable > tbody > tr > td:nth-child(2)"
        )
        product_names = [p.text.strip() for p in product_cells if p.text.strip()]
        print(f"[✓] Total product names extracted: {len(product_names)}", flush=True)
        print(f"    -> Product Names: {product_names}", flush=True)

        time.sleep(2)
        print("[✓] Part B completed successfully.", flush=True)

    except TimeoutException:
        print("[ERROR] Part B timed out waiting for table elements.", file=sys.stderr, flush=True)
    except WebDriverException as wde:
        print(f"[ERROR] Part B WebDriver failure: {wde.msg}", file=sys.stderr, flush=True)
    finally:
        if driver:
            print("[*] Closing Part B browser session...", flush=True)
            driver.quit()
            print("[✓] Session terminated cleanly.", flush=True)

def main():
    part_a_direct_child_checkbox()
    part_b_table_child_selector()
    print("\n[SUCCESS] All child selector assignments executed successfully!", flush=True)

if __name__ == "__main__":
    main()