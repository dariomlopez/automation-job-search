import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import traceback

from functions import gradual_scroll, results_folder, save_to_db

prev_count = -1

def scrape_infojobs():
    webpage = 'https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=python'
    filename = 'scraped_infojobs.csv'
    
    driver = None
    try:
        driver = Driver(uc=True)
        driver.uc_open_with_reconnect(webpage, 4)
        time.sleep(3)

        # Resolver captcha
        driver.uc_gui_click_captcha()
        time.sleep(5)

        # Aceptar cookies
        try:
            agree_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
            )
            agree_button.click()
            time.sleep(2)
        except:
            print("Botón de cookies no encontrado o ya aceptado.")

        all_jobs = []

        while True:
            gradual_scroll(driver, steps=30, pause=0.5)
            time.sleep(2)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[starts-with(@href, '//www.infojobs.net/madrid/')]"))
            )
            
            job_links = driver.find_elements(By.XPATH, "//a[starts-with(@href, '//www.infojobs.net/madrid/')]")
            
            for link in job_links:
                job_title = link.text.strip()
                job_url = link.get_attribute("href")
                
                if 'python' in job_title.lower():
                    print("Job Title:", job_title)
                    print("URL:", job_url)
                    print("-" * 40)
                    all_jobs.append((job_title, job_url))
                
            print(f"Página con {len(all_jobs)} trabajos")
            if len(all_jobs) == prev_count:
                break
            prev_count = len(all_jobs)
        
        df = pd.DataFrame(all_jobs, columns=['title', 'url'])
        file_path = results_folder(filename)
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        save_to_db(df, 'infojobs')
        
    except Exception as e:
        print(f"Error en scrape_infojobs: {e}")
        traceback.print_exc()

    finally:
        if driver:
            driver.quit()

# scrape_infojobs()