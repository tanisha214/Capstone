"""
Assignment 5: The HTML Web Table Extractor

Iterate through a multi-column HTML table, locate a row by name,
and extract a value from a neighboring column.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.w3schools.com/html/html_tables.asp")
    driver.maximize_window()

    table = wait.until(
        EC.visibility_of_element_located((By.ID, "customers"))
    )

    rows = table.find_elements(By.TAG_NAME, "tr")

    print(f"Table has {len(rows) - 1} data rows.\n")
    print("Complete Table Data:")
    print("-" * 60)

    all_data = []

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "th")

        if not cells:
            cells = row.find_elements(By.TAG_NAME, "td")

        row_data = [cell.text.strip() for cell in cells]

        if row_data:
            all_data.append(row_data)
            print(row_data)

    target_name = "Alfreds Futterkiste"

    found = False

    for row_data in all_data:

        if target_name.lower() in [cell.lower() for cell in row_data]:

            print("\n" + "-" * 60)
            print(f"FOUND ROW FOR: {target_name}")
            print(f"Complete Row: {row_data}")

            contact = row_data[1]
            country = row_data[2]

            print(f"Contact: {contact}")
            print(f"Country: {country}")

            found = True
            break

    if not found:
        print(f"\n'{target_name}' was not found in the table.")

except Exception as e:
    print(f"ERROR: {e}")

finally:
    driver.quit()