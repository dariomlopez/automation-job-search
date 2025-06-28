import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from functions import save_to_db

links = [
    'https://www.infoempleo.com/trabajo/?search=python&ordenacion=fechaAlta',
    'https://www.tecnoempleo.com/ofertas-trabajo/?te=python&pr=',
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

    if 'infoempleo' in url:
        job_header_title = soup.find_all('h2', class_='title mb15')
    elif 'tecnoempleo' in url:
        job_header_title = soup.find_all('h3', class_='fs-5 mb-2')
    
    for job_title in job_header_title:        
        # Se busca en el titulo del trabajo si contiene la palabra 'python' o 'junior'
        title = job_title.text.strip().lower()
        anchor_tag = job_title.find('a')
        
        if anchor_tag:
            # Se obtiene el atributo href del enlace
            href = anchor_tag.get('href')
            # convierte enlaces relativos en absolutos
            full_url = urljoin(url, href)
        
            if 'python' in title:
                print(f"Link: {full_url} - Title: {title}")
                jobs.append((title, full_url))
                
    return jobs if jobs else []  # Retorna lista vacía si no hay resultados

def general_job_search():
    for url in links:
        source_name = 'infoempleo' if 'infoempleo' in url else 'tecnoempleo'
        jobs = get_job_titles(url)
        if jobs:
            save_to_db(jobs, source_name)
            print(f"Guardados {len(jobs)} trabajos de {source_name}")
        else:
            print(f"No se encontraron resultados para {source_name}")

