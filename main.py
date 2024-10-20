import os, re
import pandas as pd
from login import login
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables
load_dotenv(override=True)
MEMBER_URL = os.getenv("MEMBER_URL")
driver = webdriver.Chrome()

def main():
    allScenes = []
    linkSet = set()
    
    #! LOGIN
    login(driver)

    #! GET ALL SCENES
    allScenes = findAllScenes(allScenes)
    for i in range(2,65):
        driver.get(f"{MEMBER_URL}/?page={i}")
        WebDriverWait(driver,10).until(EC.url_changes)
        allScenes = findAllScenes(allScenes)
    print(f"{len(allScenes)} scenes found")

    #! GET ALL DOWNLOAD LINKS
    for index, scene in enumerate(allScenes):
        driver.get(scene)
        WebDriverWait(driver,10).until(EC.url_changes)
        linkSet = buildLinkLibrary(linkSet)
        print(f"{index}/{len(allScenes)}")
    print(f"Link library built, {len(linkSet)} links extracted")    
    
    #! EXPORT DATA TO XLSX
    exportData('./data/data2.xlsx', linkSet,['Title', 'Download Link'])
    
    #! CLOSE DRIVER
    driver.close()
    return    

def findAllScenes(allScenes):
    try:
        # Look for "video clip" text on page and find element
        scene_links = driver.find_elements(By.XPATH, "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'video clip')]")
        for elem in scene_links:
            # Get the page link
            link = elem.get_attribute("href")
            allScenes.append(link)
    except Exception as e:
        print(e)
    return allScenes

def buildLinkLibrary(linkSet):
    title =""
    try:
        main_content = driver.find_element(By.ID, "main_content")
        sub_content = main_content.find_elements(By.TAG_NAME,"div")
        # In the first div element, find a tag and get the text
        title = sub_content[0].find_element(By.TAG_NAME,"a").text
        # Regex to drop 'page' text if any
        title = re.sub(r',?\s*page.*$', '', title).strip()
    except Exception as e:
        print(e)

    for div in sub_content:
        try:
            # Find subtitle element
            video_caption_elem = div.find_element(By.CLASS_NAME, "video_caption")
            # Add subtitle to main title for filename
            subtitle = f"{title} -- {video_caption_elem.find_element(By.TAG_NAME, "b").text.strip()}"
            # Locate download link block
            download_elem = div.find_element(By.CLASS_NAME,"media_download_block")
            # Only find elements with mp4 in its text 
            link_elem = download_elem.find_element(By.XPATH,".//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'mp4')]")
            download_link = link_elem.get_attribute('href')
            print(f"{subtitle} >> {download_link}")
            linkSet.add((subtitle,download_link))
        except Exception as e:
            continue        
    return linkSet

def exportData(filename, linkSet, columns):
    try:
        # Create a DataFrame from the linkSet
        df = pd.DataFrame(linkSet, columns=columns)        
        # Export to Excel file
        df.to_excel(filename, index=False)
        print(f"Data has been exported to {filename}")
    except Exception as e:
        print(f"Unable to export file: {e}")
    return

if __name__ ==  "__main__":
    main()