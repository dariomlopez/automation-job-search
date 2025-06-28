import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

from functions import save_to_db

def scrape_ticjob():
    os.environ["SB_CHROME_BINARY"] = "/usr/bin/chromium-browser"
    url = r'https://ticjob.es/esp/busqueda'
    searchterm = 'python'
    jobs = []
    
    driver = webdriver.Firefox()
    driver.get(url)
    
    WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'close-cookies-message'))
        ).click()
    time.sleep(2)
    

    sbox = driver.find_element(By.ID, 'keywords-input')
    sbox.send_keys(searchterm)
    print(sbox.text)

    time.sleep(5)

    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'job-card')))

    job_cards = driver.find_elements(By.CLASS_NAME, 'job-card')
    
    for card in job_cards:
        title_elem = card.find_element(By.CLASS_NAME, 'job-title')
        job_title = title_elem.text.strip().lower()

        link_elem = card.find_element(By.TAG_NAME, 'a')
        url = link_elem.get_attribute('href')
            
        if 'python' in job_title:
            jobs.append((
                job_title, url
            ))
            print(f"Job Title with python in it: {job_title}")
            print("-" * 40)
    if jobs:
        # df = pd.DataFrame(jobs, columns=['title', 'url'])
        # file_path = results_folder(filename)
        # df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"{len(jobs)} jobs found. Results saved to data base")
        save_to_db(jobs, 'ticjob')
    else:
        print("No titles containing 'python' or 'junior' found in Ticjob.")
        
    driver.quit()
    
# scrape_ticjob()