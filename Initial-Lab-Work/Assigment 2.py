"""
Assignment 2: Multiple Element Identification & Processing
Target Environment: Arch Linux, Mozilla Firefox, GeckoDriver
Techniques Demonstrated:
  - driver.find_elements(By.TAG_NAME, "a") to collect multiple link elements
  - Processing, filtering, and tabulating text and attributes from element lists
  - Interacting with multi-element collections (checkboxes: state queries and click events)
"""

import sys
import shutil
import time
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    StaleElementReferenceException,
)


def configure_firefox_driver(headless: bool = False) -> webdriver.Firefox:
    """
    Configures and initializes Mozilla Firefox using GeckoDriver on Arch Linux.

    Arch Linux package prerequisites:
      sudo pacman -S firefox geckodriver
    """
    options = FirefoxOptions()
    if headless:
        options.add_argument("-headless")

    options.add_argument("--width=1366")
    options.add_argument("--height=768")

    # Locate geckodriver binary on Arch Linux PATH
    geckodriver_bin = shutil.which("geckodriver") or "/usr/bin/geckodriver"

    try:
        service = FirefoxService(executable_path=geckodriver_bin)
        driver = webdriver.Firefox(service=service, options=options)
    except WebDriverException:
        # Fallback to Selenium Manager automatic resolution if direct path fails
        print("[INFO] Fallback: Engaging Selenium Manager for GeckoDriver...")
        driver = webdriver.Firefox(options=options)

    driver.maximize_window()
    return driver


def demonstrate_multiple_elements():
    """
    Executes multiple element identification tasks:
      Part 1: Discovering and tabulating all links (<a> tags) on the index page.
      Part 2: Finding, querying, and interacting with a collection of checkboxes.
    """
    base_url = "https://the-internet.herokuapp.com"
    driver = None

    try:
        print("=" * 80)
        print("STARTING ASSIGNMENT 2: MULTIPLE ELEMENT IDENTIFICATION")
        print("=" * 80)

        driver = configure_firefox_driver(headless=False)
        wait = WebDriverWait(driver, 10)

        print(f"\n[*] Navigating to: {base_url}")
        driver.get(base_url)

        # Ensure page content is ready
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        print("[✓] Landing page loaded successfully.")

        print("\n" + "-" * 80)
        print("PART 1: EXTRACTING AND PROCESSING ALL LINKS (TAG_NAME: 'a')")
        print("-" * 80)

        # find_elements returns a Python list of WebElement objects
        all_links: List[WebElement] = driver.find_elements(By.TAG_NAME, "a")
        total_count = len(all_links)
        print(f"[*] Total anchor ('<a>') elements detected on page: {total_count}")

        valid_links = []
        empty_text_links = 0

        print("\n{:<5} | {:<42} | {:<40}".format("No.", "Link Text", "Destination (href)"))
        print("-" * 85)

        for index, link in enumerate(all_links, start=1):
            try:
                link_text = link.text.strip()
                href = link.get_attribute("href") or "N/A"

                if link_text:
                    valid_links.append((link_text, href))
                    display_text = link_text if len(link_text) <= 40 else link_text[:37] + "..."
                    display_href = href if len(href) <= 38 else href[:35] + "..."
                    print(f"{index:<5} | {display_text:<42} | {display_href:<40}")
                else:
                    empty_text_links += 1

            except StaleElementReferenceException:
                # Handle DOM updates if elements refresh during inspection
                continue

        print("-" * 85)
        print(f"[✓] Summary of Link Extraction:")
        print(f"    - Total Links Identified   : {total_count}")
        print(f"    - Links with Visible Text  : {len(valid_links)}")
        print(f"    - Links without Text/Icons : {empty_text_links}")

        print("\n[*] Filtering Links: Finding all links starting with the letter 'C'...")
        c_links = [text for text, _ in valid_links if text.upper().startswith("C")]
        print(f"    -> Found {len(c_links)} matching links:")
        for item in c_links:
            print(f"       • {item}")

        print("\n" + "-" * 80)
        print("PART 2: WORKING WITH A COLLECTION OF INTERACTIVE ELEMENTS (CHECKBOXES)")
        print("-" * 80)

        checkbox_url = f"{base_url}/checkboxes"
        print(f"[*] Navigating to: {checkbox_url}")
        driver.get(checkbox_url)

        # Wait for checkboxes form to load
        wait.until(EC.presence_of_element_located((By.ID, "checkboxes")))

        # Locate all checkbox input elements as a list
        checkboxes: List[WebElement] = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")
        print(f"[✓] Found {len(checkboxes)} checkbox elements in the collection.\n")

        for idx, box in enumerate(checkboxes, start=1):
            is_checked_before = box.is_selected()
            print(f"[Checkbox #{idx}] Initial checked status: {is_checked_before}")

            # Toggle the checkbox state
            print(f"                 Toggling Checkbox #{idx} via .click()...")
            box.click()

            is_checked_after = box.is_selected()
            print(f"                 New checked status    : {is_checked_after}")

            # Verify the state inverted as expected
            assert is_checked_before != is_checked_after, f"Checkbox #{idx} failed to toggle state!"
            print(f"                 [✓] State change verified successfully.")

        # Pause briefly to visually inspect results when running with UI
        time.sleep(2)
        print("\n[SUCCESS] Assignment 2 completed: successfully gathered and operated on element lists!")

    except TimeoutException:
        print("[ERROR] Page request timed out waiting for DOM elements.", file=sys.stderr)
    except WebDriverException as wde:
        print(f"[ERROR] Selenium WebDriver failure: {wde.msg}", file=sys.stderr)
    finally:
        if driver:
            print("\n[*] Closing browser session...")
            driver.quit()
            print("[✓] WebDriver terminated cleanly.")


if __name__ == "__main__":
    demonstrate_multiple_elements()