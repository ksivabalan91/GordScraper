import os
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv(override=True)
LOGIN_URL = os.getenv("LOGIN_URL")

def login(driver):
    # Agree to terms and condition
    if "legal" in driver.current_url:
        try:
            agree_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "link_emphasize") and contains(., "I AGREE: ENTER")]'))
            )
            agree_button.click()
        except Exception as e:
            print(f"Error finding or clicking the button: {e}")
    
    # goto login page
    driver.get(LOGIN_URL)
    try:
        input_user = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"login")))
        input_user.send_keys(os.getenv("USERNAME"))
        input_password = driver.find_element(By.ID, "password")
        input_password.send_keys(os.getenv("PASSWORD"))
        driver.find_element(By.NAME,"commit").click()
    except Exception as e:
        print(f"Unable to login: {e}")
    return