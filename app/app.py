
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import datetime
import sqlite3
from flask import Flask, render_template
from scrapers import general_job_search, scrape_infojobs, scrape_ticjob, scrape_simplyhired
from functions import init_db


app = Flask(__name__)

# Inicializar la base de datos al inicio de la aplicación
init_db()

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


run_scrapers("general_job_search", general_job_search)
run_scrapers("infojobs", scrape_infojobs)
run_scrapers("ticjob", scrape_ticjob)
run_scrapers("simplyhired", scrape_simplyhired)


def get_db_connection():
    # Use a relative path from the app directory
    RESULTS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scrapers', 'results')
    DB_PATH = os.path.join(RESULTS_FOLDER, 'scraped_jobs.db')
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        
        return conn

    except sqlite3.Error as e:
        app.logger.error(f"Database connection error: {e}")
        raise

def get_jobs_from_db():
    today = datetime.date.today()
    conn = get_db_connection()

    cursor = conn.execute(
        'SELECT * FROM scraped_jobs WHERE date LIKE ?', (today.strftime("%Y-%m-%d"),)
    )

    jobs = cursor.fetchall()
    conn.close()

    return jobs

@app.route('/')
def index():
    jobs = get_jobs_from_db()
    return render_template('jobs.html', jobs=jobs)
    
