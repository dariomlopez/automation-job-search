# imports
import os
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback


def handle_captcha(webpage,driver=None,wait_time=10):
    """Initialize a Selenium driver, open a webpage, and handle captcha."""
    # driver = Driver(uc=True)
    # driver.get(webpage)
    # time.sleep(3)
    driver.uc_open_with_reconnect(webpage, 10)
    driver.uc_gui_click_captcha(retry=3)
    time.sleep(wait_time)
    # driver.uc_gui_click_captcha()
    # time.sleep(5)
    # return driver

# def click_cookies_button(url, button_id, driver=None):
#     try:
#         WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.ID, button_id))
#         ).click()
#         time.sleep(2)
#     except:
#         print("Botón de cookies no encontrado o ya aceptado.")
#         traceback.print_exc()
    
# --------------------
# ---- Infojobs ----
# --------------------

def gradual_scroll(driver, steps=20, pause=0.5):
    for i in range(steps):
        driver.execute_script(f"window.scrollBy(0, {i * 100});")
        time.sleep(pause)
        
def get_job_titles(soup):
    """Extrae los títulos y URLs de cada oferta de trabajo"""
    jobs = soup.find_all('h2', id='job-title')
    trabajos = []  # Lista para almacenar los trabajos
    for job in jobs:
        anchor_tag = job.find('a')
        if anchor_tag:
            title = job.text.strip()
            url = anchor_tag.get('href')
            
            if url.startswith('//'):
                url = 'https:' + url
                
            trabajos.append((title, url))  # Guardamos el título y el enlace en la lista
    return trabajos  # Retornamos todos los trabajos encontrados


def results_folder(filename: str) -> str:
    """Crea un directorio para los resultados si no existe"""
    base_dir = os.path.expanduser(
        r"C:\Users\junky\Desktop\Programacion\python\selenium_webscraping\autom_work_search\scrapers"
    )
    results_folder = os.path.join(base_dir, 'results')
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    return os.path.join(results_folder, filename)
