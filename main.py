import os, re
import pandas as pd
from login import login
from commons import timer
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# Load environment variables
load_dotenv(override=True)
MEMBER_URL: str | None = os.getenv("MEMBER_URL")
assert MEMBER_URL, "Error: MEMBER_URL is not set."

# Set options and load WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Global variables
linkSet: set = set()
exportFileName = "data2"

def main() -> None:
    #! LOGIN
    login(driver)

    #! GET ALL SCENES
    allScenes: list[str] = []
    for i in range(1, 65):
        allScenes += findAllScenes(i)
        print(f"Page: {i:,}/64")
    print(f"{len(allScenes):,} scenes found")

    #! GET ALL DOWNLOAD LINKS
    for index, scene in enumerate(allScenes):
        buildLinkLibrary(scene)
        print(f"{index+1}/{len(allScenes)}")
    print(f"Link library built, {len(linkSet)} links extracted")    
    
    #! EXPORT DATA TO XLSX
    exportData(f"./data/{exportFileName}.xlsx",dataSet=linkSet,columns=['Title', 'Download Link'])
    
    #! CLOSE DRIVER
    driver.close()
    return    

# @timer
def findAllScenes(page: int) -> list[str]:
    try:
        driver.get(f"{MEMBER_URL}/?page={page}")
        # Look for "video clip" text on page and find elements
        scene_links: list[WebElement] = driver.find_elements(By.XPATH, "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'video clip')]")
        linksToAllScenesOnPage: list[str] = [
            elem.get_attribute("href") for elem in scene_links if elem and elem.get_attribute("href") is not None
        ]  # type: ignore
        return linksToAllScenesOnPage  # Return directly from this page
    except Exception as e:
        print(f"Error on page {page}: {e}")
        return []

def buildLinkLibrary(scenePage:str) -> None:
    driver.get(scenePage)
    title: str = ""
    try:
        main_content: WebElement = driver.find_element(By.ID, "main_content")
        sub_content: list[WebElement] = main_content.find_elements(By.TAG_NAME,"div")
        # In the first div element, find a tag and get the text
        title = sub_content[0].find_element(By.TAG_NAME,"a").text
        # Regex to drop 'page' text if any
        title = re.sub(r',?\s*page.*$', '', title).strip()
    except Exception as e:
        print(e)

    for div in sub_content:
        try:
            # Find subtitle element
            video_caption_elem: WebElement = div.find_element(By.CLASS_NAME, "video_caption")
            # Add subtitle to main title for filename
            subtitle: str = f"{title} -- {video_caption_elem.find_element(By.TAG_NAME, "b").text.strip()}"
            # Locate download link block
            download_elem: WebElement = div.find_element(By.CLASS_NAME,"media_download_block")
            # Only find elements with mp4 in its text 
            link_elem: WebElement = download_elem.find_element(By.XPATH,".//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'mp4')]")
            download_link: str | None = link_elem.get_attribute('href')
            print(f"{subtitle} >> {download_link}")
            linkSet.add((subtitle,download_link))
        except Exception as e:
            continue        

def exportData(filename, dataSet, columns) -> None:
    try:
        # Create a DataFrame from the linkSet
        df = pd.DataFrame(dataSet, columns=columns)        
        # Export to Excel file
        df.to_excel(filename, index=False)
        print(f"Data has been exported to {filename}")
    except Exception as e:
        print(f"Unable to export file: {e}")
    return

if __name__ ==  "__main__":
    main()