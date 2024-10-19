import os, re, csv, time
from login import login
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
    allScenes = []
    linkSet = set()
    
    #! LOGIN
    driver.get(MEMBER_URL)
    for i in range(1, MAX_ATTEMPTS +1):
        if("mem" not in driver.current_url):
            print(f"Login attempt:{i}")
            login(driver)
        else:
            break
    print("Successfully logged in!")

    #! GET ALL SCENES
    allScenes = findAllScenes(allScenes)
    for i in range(2,3):
        driver.get(f"{MEMBER_URL}/?page={i}")
        WebDriverWait(driver,10).until(EC.url_changes)
        allScenes = findAllScenes(allScenes)
    print(f"{len(allScenes)} scenes found")

    #! GET ALL DOWNLOAD LINKS
    for scene in allScenes:
        driver.get(scene)
        WebDriverWait(driver,10).until(EC.url_changes)
        linkSet = buildLinkLibrary(linkSet)
    print(f"Link library built, {len(linkSet)} links extracted")    
    
    #! Export data to CSV
    exportData('data.csv', linkSet)
    
    driver.close()
    return    

def findAllScenes(allScenes):
    scene_links = driver.find_elements(By.XPATH, "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'video clip')]")
    for elem in scene_links:
        link = elem.get_attribute("href")
        allScenes.append(link)
    return allScenes

def buildLinkLibrary(linkSet):
    main_content = driver.find_element(By.ID, "main_content")
    sub_content = main_content.find_elements(By.TAG_NAME,"div")
    
    title = sub_content[0].find_element(By.TAG_NAME,"a").text
    title = re.sub(r',?\s*page.*$', '', title).strip()

    for div in sub_content:
        try:
            video_caption_elem = div.find_element(By.CLASS_NAME, "video_caption")
            subtitle = f"{title} -- {video_caption_elem.find_element(By.TAG_NAME, "b").text.strip()}"
            download_elem = div.find_element(By.CLASS_NAME,"media_download_block")
            link_elem = download_elem.find_element(By.XPATH,".//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'mp4')]")
            download_link = link_elem.get_attribute('href')
            print(f"{subtitle} >> {download_link}")
            linkSet.add((subtitle,download_link))
        except Exception as e:
            continue        
    return linkSet

def exportData(filename, linkSet):
    with open(filename,mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title','Download Link'])
        for subtitle, link in linkSet:
            writer.writerow([subtitle,link])
    print(f"Data has been exported to {filename}")
    return

if __name__ ==  "__main__":
    main()