import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

from functions import results_folder

links = [
    'https://weworkremotely.com/categories/remote-back-end-programming-jobs#job-listings',
    'https://www.infoempleo.com/trabajo/?search=python&ordenacion=fechaAlta',
    'https://www.tecnoempleo.com/ofertas-trabajo/?te=python&pr='
    ]


def get_job_titles(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    jobs = []
    response = requests.get(url, stream=True, headers=headers)

    # print(response.status_code)

    page = response.content
    soup = BeautifulSoup(page, 'html.parser')

    if 'weworkremotely' in url:
        job_header_title = soup.find_all('h4',class_='new-listing__header__title')
    elif 'infoempleo' in url:
        job_header_title = soup.find_all('h2', class_='title mb15')
    elif 'tecnoempleo' in url:
        job_header_title = soup.find_all('h3', class_='fs-5 mb-2')
    
    for job_title in job_header_title:
        # job_title es la etiqueta HTML que  el título del trabajo
            # print(job_title)
        # job_title.text es el texto dentro de la etiqueta HTML
            # print(job_title.text)
            
        # Se busca en el titulo del trabajo si contiene la palabra 'python' o 'junior'
        title = job_title.text.strip().lower()
        anchor_tag = job_title.find('a')
        
        if anchor_tag:
            # Se obtiene el atributo href del enlace
            href = anchor_tag.get('href')
            # convierte enlaces relativos en absolutos
            full_url = urljoin(url, href)
        
            if 'python' in title or 'junior' in title:
                print(f"Link: {full_url} - Title: {title}")
                jobs.append((title, full_url))
                
    if jobs:
        df = pd.DataFrame(jobs, columns=['title', 'url'])
        return df
    return pd.DataFrame(columns=['title', 'url'])  # Retorna DF vacío si no hay resultados

def general_job_search():
    all_jobs = []
    for url in links:
        df = get_job_titles(url)
        if not df.empty:
            all_jobs.append(df)
    
    if all_jobs:
        final_df = pd.concat(all_jobs, ignore_index=True)
        filename = 'general_jobs.csv'
        file_path = results_folder(filename)
        final_df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"\nArchivo guardado en: {file_path}\n")
        return final_df
    return pd.DataFrame(columns=['title', 'url'])
