
import os
import datetime
import sqlite3
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Ruta donde se encuentran los resultados
#RESULTS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scrapers', 'results')

DB_PATH = os.path.join('/tmp', 'scraped_jobs.db')

def get_db_connection():
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
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
        'SELECT * FROM scraped_jobs WHERE date = ?', (today,)
    )

    jobs = cursor.fetchall()
    conn.close()

    return jobs

@app.route('/')
def index():
    jobs = get_jobs_from_db()
    return render_template('jobs.html', jobs=jobs)
    
