import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
import time

from functions import handle_captcha, save_to_db

base_url = 'https://www.simplyhired.es'

def scrape_simplyhired():
    website = 'https://www.simplyhired.es/search?q=python&l='
    # filename = 'scraped_simplyhired.csv'
    all_jobs = []
    
    driver = Driver(uc=True)
    handle_captcha(website, driver=driver)
    time.sleep(10)
    WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//h2[@data-testid='searchSerpJobTitle']"))
        )
    job_urls = driver.find_elements(By.XPATH, "//h2[@data-testid='searchSerpJobTitle']/a")
    
    for url in job_urls:
        title = url.text.strip()
        url = url.get_attribute('href')

        if 'python' in title.lower():
            print("Job Title:", title)
            print("URL:", base_url + url if url.startswith("/") else url)
            print("-" * 40)
            all_jobs.append((title, url))
    
    # df = pd.DataFrame(all_jobs, columns=['title', 'url'])
    # file_path = results_folder(filename)
    # df.to_csv(file_path, index=False, encoding='utf-8-sig')
    save_to_db(all_jobs, 'simplyhired')
    driver.quit()
    
# scrape_simplyhired()