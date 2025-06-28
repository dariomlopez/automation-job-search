import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers import general_job_search, scrape_infojobs, scrape_ticjob, scrape_simplyhired

def run_scrapers(nombre, scraper_function):
    """
    Ejecuta un scraper y guarda los resultados en la base de datos.
    
    :param nombre: Nombre del scraper.
    :param scraper_function: Función del scraper a ejecutar.
    """
    try:
        print(f"Ejecutando scraper {nombre}...")
        scraper_function()

        print(f"Resultados de {nombre} guardados en la base de datos.")
    except Exception as e:
        print(f"Error al ejecutar el scraper {nombre}: {str(e)}")

def main():
    run_scrapers("general_job_search", general_job_search)
    run_scrapers("infojobs", scrape_infojobs)
    run_scrapers("ticjob", scrape_ticjob)
    run_scrapers("simplyhired", scrape_simplyhired)
    # run_scrapers("indeed", scrape_indeed)

if __name__ == "__main__":
    main()
