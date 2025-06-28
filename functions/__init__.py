
# imports
import os
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3

# RESULTS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scrapers', 'results')

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


def save_to_db(jobs, sources):
    """Guarda los trabajos en una base de datos SQLite."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'scrapers', 'results', 'scraped_jobs.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Crear la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraped_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT,
            source TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insertar los trabajos
    if isinstance(sources, str):
        cursor.executemany('INSERT INTO scraped_jobs (title, url, source) VALUES (?, ?, ?)', [(title, url, sources) for title, url in jobs])
    else:
        cursor.executemany('INSERT INTO scraped_jobs (title, url, source) VALUES (?, ?, ?)', [(title, url, source) for (title, url), source in zip(jobs, sources)])
    
    conn.commit()
    conn.close()
