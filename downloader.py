import os
import pandas as pd
from login import login
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

load_dotenv(override=True)

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")
EXTENSION_DIRECTORY=os.getenv("EXTENSION_DIRECTORY")
MAX_ATTEMPTS = 3

#! SET UP CHROME DRIVER
chrome_options = Options()
# chrome_options.add_extension(EXTENSION_DIRECTORY)
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_DIR,  # Set download directory
    "download.prompt_for_download": False,  # Disable download prompt
    "download.directory_upgrade": True,  # Allow directory upgrade
    "safebrowsing.enabled": True  # Enable safe browsing
})
driver = webdriver.Chrome(options=chrome_options)

def startDownload():
    #! LOGIN
    login(driver)
    
    #! LOAD DATA
    df = loadData("./data/data.xlsx")
    linkList = df["Download Link"].to_list()
    
    #! MAKE GET REQUESTS TO DOWNLOAD LINKS
    for index,link in enumerate(linkList):
        print(f"Making get request for {link}")
        driver.get(link)
        print(f"{index}/{len(linkList)}")

    driver.close()
    
def loadData(filename):
    try:        
        df = pd.read_excel(filename)        
    except FileNotFoundError as e:
        print("File not found")        
    return df
        
if __name__ == "__main__":
    startDownload()
