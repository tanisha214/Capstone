from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize Firefox
driver = webdriver.Firefox()
driver.maximize_window()

# 1. Open the 1st URL
driver.get("https://testautomationpractice.blogspot.com/")

# Store original window handle
parent_window = driver.current_window_handle
print("Parent Window ID:", parent_window)

# 2. Click button/link to open a new tab/window
new_tab_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'New Browser Window') or contains(text(), 'New Tab')]")
new_tab_btn.click()

# Wait until second window appears
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

# Get all window handles
all_windows = driver.window_handles
print("All Windows:", all_windows)

# 3. Switch to the new window/tab
for handle in all_windows:
    if handle != parent_window:
        driver.switch_to.window(handle)
        break

# Perform an action on the new tab
print("Title of new tab:", driver.title)
time.sleep(2)

# 4. Close the new tab
driver.close()

# 5. Switch back to the original window
driver.switch_to.window(parent_window)

# Enter your name in a text field on the original page
name_input = driver.find_element(By.ID, "name")
name_input.clear()
name_input.send_keys("John Doe")

time.sleep(2)
driver.quit()
