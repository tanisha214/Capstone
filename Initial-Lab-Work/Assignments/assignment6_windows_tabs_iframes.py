"""
Assignment 6: Windows, Tabs, and Iframes

Interact with an element inside an iframe, open a new tab,
switch context, read its title, close it, and switch back
to the original tab.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ---------------------------------------------------------
# Initialize Chrome
# ---------------------------------------------------------

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

try:

    # =====================================================
    # PART 1: IFRAME INTERACTION
    # =====================================================

    print("--- IFRAME INTERACTION ---")

    driver.get("https://www.w3schools.com/html/html_iframe.asp")
    driver.maximize_window()

    print(f"Main page title: {driver.title}")

    # Locate the iframe
    iframe = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "iframe")
        )
    )

    print("Iframe located.")

    # Switch into iframe
    wait.until(
        EC.frame_to_be_available_and_switch_to_it(iframe)
    )

    print("Switched into iframe.")

    # Read content inside iframe
    iframe_body = wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    print("Iframe content:")
    print(iframe_body.text[:200])

    # Return to main document
    driver.switch_to.default_content()

    print("Switched back to main page.")


    # =====================================================
    # PART 2: NEW TAB HANDLING
    # =====================================================

    print("\n--- NEW TAB HANDLING ---")

    # Store original window
    main_window = driver.current_window_handle

    print(f"Main window handle: {main_window}")

    # Store current windows
    existing_windows = set(driver.window_handles)

    # Open Google in a new tab
    driver.execute_script(
        "window.open('https://www.google.com', '_blank');"
    )

    # Wait for new tab
    wait.until(
        lambda d: len(d.window_handles) > len(existing_windows)
    )

    # Get all windows
    all_windows = driver.window_handles

    print(f"Total windows open: {len(all_windows)}")

    # Find the new window
    new_window = next(
        handle for handle in all_windows
        if handle != main_window
    )

    # Switch to new tab
    driver.switch_to.window(new_window)

    print("Switched to new tab.")

    # Wait for Google title
    wait.until(
        EC.title_contains("Google")
    )

    print(f"New tab title: '{driver.title}'")


    # =====================================================
    # PART 3: CLOSE NEW TAB
    # =====================================================

    driver.close()

    print("New tab closed.")

    # Switch back to original tab
    driver.switch_to.window(main_window)

    print("Switched back to original tab.")
    print(f"Current title: '{driver.title}'")

    print("\nAssignment 6 completed successfully.")


except Exception as e:

    print("\nERROR:")
    print(type(e).__name__)
    print(e)


finally:

    driver.quit()