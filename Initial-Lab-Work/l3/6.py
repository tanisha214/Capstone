import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

os.makedirs("screenshots", exist_ok=True)

driver = webdriver.Firefox()

def capture_step(driver, step_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"screenshots/{step_name}_{timestamp}.png"
    driver.save_screenshot(file_path)
    print(f"Captured: {file_path}")

driver.get("https://testautomationpractice.blogspot.com/")
capture_step(driver, "01_homepage_loaded")

driver.find_element(By.ID, "name").send_keys("Automated User")
capture_step(driver, "02_name_entered")

driver.find_element(By.ID, "male").click()
capture_step(driver, "03_gender_selected")

driver.quit()
