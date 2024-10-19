import os, re, csv, time
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

# Set up Chrome options
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_DIR,  # Set download directory
    "download.prompt_for_download": False,  # Disable download prompt
    "download.directory_upgrade": True,  # Allow directory upgrade
    "safebrowsing.enabled": True  # Enable safe browsing
})
driver = webdriver.Chrome(options=chrome_options)
