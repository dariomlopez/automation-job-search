
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import datetime
import sqlite3
from flask import Flask, render_template
from functions import init_db

app = Flask(__name__)

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
    
if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run()
