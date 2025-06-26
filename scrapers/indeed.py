import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

from functions import results_folder, save_to_db

def scrape_indeed():
    base_url = 'https://es.indeed.com'
    website = f"{base_url}/jobs?q=python&l=&sort=date"
    # searchterm = 'python'
    filename = 'scraped_indeed.csv'
    all_jobs = []
    
    driver = Driver(uc=True)
    driver.uc_open_with_reconnect(website, 6)
    time.sleep(3)

    # Resolver captcha
    driver.uc_gui_click_captcha()
    time.sleep(2)
    driver.uc_gui_click_captcha()
    time.sleep(2)
    driver.uc_gui_handle_captcha()
    time.sleep(2)
    driver.uc_gui_handle_captcha()
    time.sleep(2)
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[starts-with(@href, '/rc/clk') and @data-jk]"))
    )
    
    job_links = driver.find_elements(By.XPATH, "//a[starts-with(@href, '/rc/clk') and @data-jk]")

    for link in job_links:
        title = link.text.strip()
        href = link.get_attribute("href")
    
        if 'python' in title.lower():
            print("Job Title:", title)
            print("URL:", base_url + href if href.startswith("/") else href)
            print("-" * 40)
            all_jobs.append((title, href))
    save_to_db(all_jobs, 'indeed')
    # df = pd.DataFrame(all_jobs, columns=['title', 'url'])
    # file_path = results_folder(filename)
    # df.to_csv(file_path, index=False, encoding='utf-8-sig')
    driver.quit()
# scrape_indeed()