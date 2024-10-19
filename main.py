import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


load_dotenv(override=True)
LOGIN_URL = os.getenv("LOGIN_URL")
MEMBER_URL = os.getenv("MEMBER_URL")
MAX_ATTEMPTS = 3
driver = webdriver.Chrome()

def main():
    driver.get(MEMBER_URL)
    for i in range(1, MAX_ATTEMPTS +1):
        if("mem" not in driver.current_url):
            print(f"Login attempt:{i}")
            login()
        else:
            break
    print("Successfully logged in!")
    
    time.sleep(15)
    driver.close()
    return
    

def login():
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
    except:
        print(f"Unable to login: {e}")

    return   

if __name__ ==  "__main__":
    main()
