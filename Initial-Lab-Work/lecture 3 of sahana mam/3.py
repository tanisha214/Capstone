import os
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://testautomationpractice.blogspot.com/")

# Locate file input element
file_input = driver.find_element(By.ID, "singleFileInput")

# Absolute path of the file to upload
file_path = os.path.abspath("sample.txt")

# Send the path directly to the input element
file_input.send_keys(file_path)

# Click upload button if required
upload_button = driver.find_element(By.XPATH, "//button[text()='Upload Single File']")
upload_button.click()
