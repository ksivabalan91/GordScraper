import os
import pandas as pd
from pandas import DataFrame
from login import login
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Load environment variables
load_dotenv(override=True)
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")
EXTENSION_DIRECTORY = os.getenv("EXTENSION_DIRECTORY")
assert DOWNLOAD_DIR,"Error: DOWNLOAD_DIR is not set."
assert EXTENSION_DIRECTORY,"Error: EXTENSION_DIRECTORY is not set."

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

def startDownload() -> None:
    #! LOGIN
    login(driver)
    
    #! LOAD DATA
    df: DataFrame = loadData("./data/data.xlsx")
    linkList = df["Download Link"].to_list()
    
    #! MAKE GET REQUESTS TO DOWNLOAD LINKS
    for index,link in enumerate(linkList):
        print(f"Making get request for {link}")
        driver.get(link)
        print(f"{index:,}/{len(linkList):,}")

    driver.close()
    
def loadData(filename):
    try:        
        df: DataFrame = pd.read_excel(filename)        
    except:
        raise FileNotFoundError(f"{filename} not found")        
    return df
        
if __name__ == "__main__":
    startDownload()
