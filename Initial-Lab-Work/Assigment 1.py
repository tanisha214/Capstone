"""
Assignment 1: Web Element Identification
Target Environment: Arch Linux, Mozilla Firefox, GeckoDriver
Locators demonstrated: By.ID, By.NAME, By.TAG_NAME, By.LINK_TEXT, By.CLASS_NAME
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
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)


def configure_firefox_driver(headless: bool = False) -> webdriver.Firefox:
    """
    Configures and initializes Mozilla Firefox using GeckoDriver on Arch Linux.

    Arch Linux package references:
      - firefox: sudo pacman -S firefox
      - geckodriver: sudo pacman -S geckodriver
    """
    options = FirefoxOptions()

    if headless:
        # Headless mode execution (useful for headless servers or CI runners)
        options.add_argument("-headless")

    # Standard desktop screen dimension
    options.add_argument("--width=1280")
    options.add_argument("--height=900")

    # Arch Linux typically places geckodriver in /usr/bin/geckodriver
    geckodriver_path = shutil.which("geckodriver") or "/usr/bin/geckodriver"

    try:
        service = FirefoxService(executable_path=geckodriver_path)
        driver = webdriver.Firefox(service=service, options=options)
    except WebDriverException:
        # Fallback to Selenium 4.x automatic Selenium Manager if explicit path fails
        print("[INFO] Fallback: Letting Selenium Manager locate geckodriver automatically...")
        driver = webdriver.Firefox(options=options)

    driver.maximize_window()
    return driver


def demonstrate_element_locators():
    """
    Navigates to the industry-standard test page and locates target elements
    using By.ID, By.NAME, By.TAG_NAME, By.LINK_TEXT, and By.CLASS_NAME.
    """
    target_url = "https://the-internet.herokuapp.com/login"
    driver = None

    try:
        print("=" * 70)
        print("Initializing Firefox WebDriver on Arch Linux...")
        print("=" * 70)
        driver = configure_firefox_driver(headless=False)

        print(f"[*] Navigating to: {target_url}")
        driver.get(target_url)

        # Explicit wait setup (10-second ceiling)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
        print("[✓] Webpage successfully loaded.\n")

        print("-" * 70)
        print("EXECUTING ELEMENT IDENTIFICATION & VERIFICATION")
        print("-" * 70)

        # 1. By.ID Locator: Locate the Username input field
        print("\n[1] Strategy: By.ID")
        username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
        print(f"    -> Located Element : <{username_field.tag_name}>")
        print(f"    -> Attribute 'id'   : {username_field.get_attribute('id')}")
        print(f"    -> Attribute 'type' : {username_field.get_attribute('type')}")
        username_field.clear()
        username_field.send_keys("tomsmith")
        print("    -> Action Performed : Entered test credentials into username field.")

        # 2. By.NAME Locator: Locate the Password input field
        print("\n[2] Strategy: By.NAME")
        password_field = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
        print(f"    -> Located Element : <{password_field.tag_name}>")
        print(f"    -> Attribute 'name' : {password_field.get_attribute('name')}")
        print(f"    -> Attribute 'type' : {password_field.get_attribute('type')}")
        password_field.clear()
        password_field.send_keys("SuperSecretPassword!")
        print("    -> Action Performed : Entered secret password into password field.")

        # 3. By.TAG_NAME Locator: Locate the Main Header (h2)
        print("\n[3] Strategy: By.TAG_NAME")
        header_element = driver.find_element(By.TAG_NAME, "h2")
        print(f"    -> Located Element : <{header_element.tag_name}>")
        print(f"    -> Header Text     : '{header_element.text.strip()}'")

        # 4. By.CLASS_NAME Locator: Locate Subheader instruction text and Login Button
        print("\n[4] Strategy: By.CLASS_NAME")
        subheader_element = driver.find_element(By.CLASS_NAME, "subheader")
        print(f"    -> Located Element : <{subheader_element.tag_name}>")
        print(f"    -> Class Attribute : '{subheader_element.get_attribute('class')}'")
        print(f"    -> Text Content    : '{subheader_element.text.strip()}'")

        login_button = driver.find_element(By.CLASS_NAME, "radius")
        print(f"    -> Located Button  : Class='{login_button.get_attribute('class')}'")
        print(f"    -> Button Text     : '{login_button.text.strip()}'")

        # 5. By.LINK_TEXT Locator: Locate the Footer link by its exact anchor text
        print("\n[5] Strategy: By.LINK_TEXT")
        footer_link = driver.find_element(By.LINK_TEXT, "Elemental Selenium")
        print(f"    -> Located Element : <{footer_link.tag_name}>")
        print(f"    -> Link Text Match : '{footer_link.text}'")
        print(f"    -> Target URL (href): {footer_link.get_attribute('href')}")

        print("\n" + "-" * 70)
        print("VERIFYING WORKFLOW: SUBMITTING FORM WITH LOCATED ELEMENTS")
        print("-" * 70)

        # Click the login button identified by class name
        login_button.click()

        # Wait for the flash banner indicating successful authentication
        flash_banner = wait.until(EC.visibility_of_element_located((By.ID, "flash")))
        print(f"[✓] Post-Action Banner (By.ID 'flash'): {flash_banner.text.strip()}")

        # Verify success message confirmation
        if "You logged into a secure area!" in flash_banner.text:
            print("[SUCCESS] All 5 locator methods verified and functional!")
        else:
            print("[WARN] Login state differed from expected.")

        # Pause briefly to visually inspect results in non-headless mode
        time.sleep(2)

    except NoSuchElementException as nse:
        print(f"[ERROR] Failed to locate element: {nse.msg}", file=sys.stderr)
    except TimeoutException:
        print("[ERROR] Timed out waiting for element presence or visibility.", file=sys.stderr)
    except WebDriverException as wde:
        print(f"[ERROR] WebDriver issue on Arch Linux: {wde.msg}", file=sys.stderr)
        print("\nTip: Ensure geckodriver and firefox are installed via pacman:")
        print("     sudo pacman -S firefox geckodriver")
    finally:
        if driver:
            print("\n[*] Terminating Firefox browser session...")
            driver.quit()
            print("[✓] Session terminated cleanly.")


if __name__ == "__main__":
    demonstrate_element_locators()