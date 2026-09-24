"""
Assignment 8: Data-Driven Automation (DDT)

Reads multiple login test cases from an external CSV file
using Pandas and executes each test case through Selenium.

CSV columns:
    username
    password
    expected_result

Expected results:
    PASS
    FAIL
"""

from pathlib import Path

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException
)


# =========================================================
# 1. LOAD CSV DATA
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

CSV_FILE = BASE_DIR / "data" / "login_test_data.csv"

print("CSV file location:")
print(CSV_FILE)

# Check whether CSV exists
if not CSV_FILE.exists():
    raise FileNotFoundError(
        f"\nCSV file not found:\n{CSV_FILE}"
    )

# Read CSV
test_data = pd.read_csv(
    CSV_FILE,
    keep_default_na=False
)

print(f"\nLoaded {len(test_data)} test cases from CSV.\n")

print("Test Data:")
print("-" * 70)
print(test_data)
print("-" * 70)


# =========================================================
# 2. VALIDATE CSV COLUMNS
# =========================================================

required_columns = {
    "username",
    "password",
    "expected_result"
}

missing_columns = required_columns - set(test_data.columns)

if missing_columns:
    raise ValueError(
        f"Missing columns in CSV: {missing_columns}"
    )


# =========================================================
# 3. START CHROME
# =========================================================

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)

results_summary = []


# =========================================================
# 4. DATA-DRIVEN TEST EXECUTION
# =========================================================

try:

    for index, row in test_data.iterrows():

        test_number = index + 1

        username = str(row["username"]).strip()
        password = str(row["password"]).strip()
        expected_result = str(
            row["expected_result"]
        ).strip().upper()

        print("\n" + "=" * 70)
        print(f"TEST CASE {test_number}")
        print("=" * 70)

        print(f"Username       : {username}")
        print(f"Password       : {password}")
        print(f"Expected Result: {expected_result}")

        actual_result = "UNKNOWN"
        status = "FAILED"

        try:

            # -------------------------------------------------
            # Open SauceDemo login page
            # -------------------------------------------------

            driver.get(
                "https://www.saucedemo.com/"
            )

            # -------------------------------------------------
            # Locate username field
            # -------------------------------------------------

            username_field = wait.until(
                EC.visibility_of_element_located(
                    (By.ID, "user-name")
                )
            )

            # -------------------------------------------------
            # Locate password field
            # -------------------------------------------------

            password_field = wait.until(
                EC.visibility_of_element_located(
                    (By.ID, "password")
                )
            )

            # -------------------------------------------------
            # Enter username
            # -------------------------------------------------

            username_field.clear()

            if username:
                username_field.send_keys(username)

            # -------------------------------------------------
            # Enter password
            # -------------------------------------------------

            password_field.clear()

            if password:
                password_field.send_keys(password)

            # -------------------------------------------------
            # Locate Login button
            # -------------------------------------------------

            login_button = wait.until(
                EC.presence_of_element_located(
                    (By.ID, "login-button")
                )
            )

            # Scroll button into view
            driver.execute_script(
                "arguments[0].scrollIntoView({"
                "block: 'center'"
                "});",
                login_button
            )

            # Wait until clickable
            wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "login-button")
                )
            )

            # -------------------------------------------------
            # Click Login
            # -------------------------------------------------

            try:

                login_button.click()

            except ElementClickInterceptedException:

                # Fallback if another page element intercepts click
                driver.execute_script(
                    "arguments[0].click();",
                    login_button
                )

            # -------------------------------------------------
            # Determine actual result
            # -------------------------------------------------

            try:

                # Successful login redirects to inventory.html
                wait.until(
                    EC.url_contains("inventory.html")
                )

                actual_result = "PASS"

                print("\nActual Result  : PASS")
                print("Login successful.")

            except TimeoutException:

                # Login did not redirect.
                # Check whether SauceDemo displayed an error.

                try:

                    error_message = wait.until(
                        EC.visibility_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                "[data-test='error']"
                            )
                        )
                    )

                    actual_result = "FAIL"

                    print("\nActual Result  : FAIL")
                    print(
                        f"Error Message  : "
                        f"{error_message.text}"
                    )

                except TimeoutException:

                    actual_result = "FAIL"

                    print(
                        "\nActual Result  : FAIL"
                    )

                    print(
                        "Login failed, but no "
                        "error message was detected."
                    )

            # -------------------------------------------------
            # Compare actual vs expected result
            # -------------------------------------------------

            if actual_result == expected_result:

                status = "PASSED"

                print("✅ TEST PASSED")

            else:

                status = "FAILED"

                print(
                    "❌ TEST FAILED "
                    f"(Expected: {expected_result}, "
                    f"Actual: {actual_result})"
                )

        except Exception as e:

            actual_result = "ERROR"
            status = "FAILED"

            print("\n❌ ERROR DURING TEST CASE")
            print(type(e).__name__)
            print(e)

        # -----------------------------------------------------
        # Store result
        # -----------------------------------------------------

        results_summary.append({
            "Test Case": test_number,
            "Username": username,
            "Expected": expected_result,
            "Actual": actual_result,
            "Status": status
        })


# =========================================================
# 5. FINAL SUMMARY
# =========================================================

finally:

    print("\n" + "=" * 70)
    print("DATA-DRIVEN TEST EXECUTION SUMMARY")
    print("=" * 70)

    for result in results_summary:

        print(
            f"Test Case {result['Test Case']} | "
            f"Username: {result['Username']} | "
            f"Expected: {result['Expected']} | "
            f"Actual: {result['Actual']} | "
            f"{result['Status']}"
        )

    total = len(results_summary)

    passed = sum(
        1
        for result in results_summary
        if result["Status"] == "PASSED"
    )

    failed = total - passed

    print("\n" + "-" * 70)
    print(f"Total Test Cases : {total}")
    print(f"Passed           : {passed}")
    print(f"Failed           : {failed}")
    print("-" * 70)

    driver.quit()

    print("\nBrowser closed.")
    print("Assignment 8 execution completed.")