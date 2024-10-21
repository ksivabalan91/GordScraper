import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables
load_dotenv(override=True)
MEMBER_URL = os.getenv("MEMBER_URL")
LOGIN_URL = os.getenv("LOGIN_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Assert that the environment variables are set
assert MEMBER_URL, "Error: MEMBER_URL is not set."
assert LOGIN_URL, "Error: LOGIN_URL is not set."
assert USERNAME, "Error: USERNAME is not set."
assert PASSWORD, "Error: PASSWORD is not set."

def login(driver) -> None: 
    driver.get(MEMBER_URL)
    wait = WebDriverWait(driver,10)
    # if redirected to /legal page, agree to agree to terms and conditions
    if "legal" in driver.current_url:
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "link_emphasize") and contains(., "I AGREE: ENTER")]'))).click()
        except:
            raise Exception(f"Error finding or clicking 'I AGREE' the button")
    
    # Go to login page
    driver.get(LOGIN_URL)
    try:
        # Input credentials
        wait.until(EC.element_to_be_clickable((By.ID,"login"))).send_keys(USERNAME) # type: ignore
        wait.until(EC.element_to_be_clickable((By.ID,"password"))).send_keys(PASSWORD) # type: ignore
        wait.until(EC.element_to_be_clickable((By.NAME,"commit"))).click()
    except:
        raise Exception(f"Unable to login")