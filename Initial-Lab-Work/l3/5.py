from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://testautomationpractice.blogspot.com/")

# Method 1: save_screenshot()
driver.save_screenshot("homepage_screenshot.png")

# Method 2: get_screenshot_as_file()
driver.get_screenshot_as_file("./screenshots/login_page.png")

# Method 3: Screenshot of a specific element
table = driver.find_element(By.NAME, "BookTable")
table.screenshot("table_element.png")

driver.quit()
