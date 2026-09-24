from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://testautomationpractice.blogspot.com/")

# Locate the table
table = driver.find_element(By.NAME, "BookTable")

# 1. Total rows and columns
rows = table.find_elements(By.XPATH, ".//tr")
total_rows = len(rows)
cols = table.find_elements(By.XPATH, ".//tr[1]/th")
total_cols = len(cols)

print(f"Total Rows: {total_rows}, Total Columns: {total_cols}")

# 2. Iterate through rows and extract data
for row_idx in range(2, total_rows + 1):  # Starting at 2 to skip headers
    book_name = driver.find_element(By.XPATH, f"//table[@name='BookTable']//tr[{row_idx}]/td[1]").text
    author = driver.find_element(By.XPATH, f"//table[@name='BookTable']//tr[{row_idx}]/td[2]").text
    price = driver.find_element(By.XPATH, f"//table[@name='BookTable']//tr[{row_idx}]/td[4]").text

    # Conditional action: identify books with price <= 500
    if int(price) <= 500:
        print(f"[Match] Book: {book_name} | Author: {author} | Price: {price}")

driver.quit()
