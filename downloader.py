import os, time, random
import pandas as pd
from login import login
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

load_dotenv(override=True)

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")
MEMBER_URL = os.getenv("MEMBER_URL")
EXTENSION_DIRECTORY=os.getenv("EXTENSION_DIRECTORY")
MAX_ATTEMPTS = 3

# Set up Chrome options
chrome_options = Options()
chrome_options.add_extension(EXTENSION_DIRECTORY)
# chrome_options.add_experimental_option("prefs", {
#     "download.default_directory": DOWNLOAD_DIR,  # Set download directory
#     "download.prompt_for_download": False,  # Disable download prompt
#     "download.directory_upgrade": True,  # Allow directory upgrade
#     "safebrowsing.enabled": True  # Enable safe browsing
# })
driver = webdriver.Chrome(options=chrome_options)

def startDownload():
    #! LOGIN
    driver.get(MEMBER_URL)
    for i in range(1, MAX_ATTEMPTS +1):
        if("mem" not in driver.current_url):
            print(f"Login attempt:{i}")
            login(driver)
        else:
            break
    print("Successfully logged in!")
    
    df = loadData("data.xlsx")
    linkList = df["Download Link"].to_list()
    
    for index,link in enumerate(linkList):
        print(f"Making get request for {link}")
        driver.get(link)
        # time.sleep(2)
        # Pause after every 20 links
        if (index + 1) % 30 == 0:  # Use (index + 1) because index is zero-based
            pause_duration = random.randint(5,10)
            print(f"Pausing for {pause_duration} seconds...")
            time.sleep(pause_duration)  # Pause for 10 seconds
            
    driver.close()
    
    return
def loadData(filename):
    try:        
        df = pd.read_excel(filename)        
    except FileNotFoundError as e:
        print("File not found")
        
    return df
        
if __name__ == "__main__":
    startDownload()
