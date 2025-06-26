import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers import general_job_search, scrape_infojobs, scrape_ticjob, scrape_indeed, scrape_simplyhired

def run_scrapers(nombre, scraper_function):
    """
    Ejecuta un scraper y guarda los resultados en un archivo CSV.
    
    :param nombre: Nombre del scraper (usado para el nombre del archivo).
    :param scraper_function: Función del scraper a ejecutar.
    """
    try:
        print(f"Ejecutando scraper {nombre}...")
        results = scraper_function()
        if results is None or (hasattr(results, 'empty') and results.empty):
            print(f"No se encontraron resultados para {nombre}.")
            return
        
        filename = f"scraped_{nombre}.csv"
        file_path = os.path.join("scrapers", "results", filename)
        
        results.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"Resultados guardados en {file_path}")
    except Exception as e:
        print(f"Error al ejecutar el scraper {nombre}: {str(e)}")

def main():
    # Asegurar que existe el directorio de resultados
    os.makedirs(os.path.join("scrapers", "results"), exist_ok=True)
    
    run_scrapers("general_job_search", general_job_search)
    run_scrapers("infojobs", scrape_infojobs)
    run_scrapers("ticjob", scrape_ticjob)
    run_scrapers("simplyhired", scrape_simplyhired)
    run_scrapers("indeed", scrape_indeed)

if __name__ == "__main__":
    main()
