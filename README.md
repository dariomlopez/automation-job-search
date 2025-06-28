# 🐍 Python Job Scraper & Visualizer
An automated job search assistant focused on finding Python Developer roles.
It scrapes job listings from selected platforms and displays them via a Flask app.

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Selenium](https://img.shields.io/badge/Automation-Selenium-informational)
![Flask](https://img.shields.io/badge/Flask-2.3-blue?logo=flask&logoColor=white)
![SQLite Powered](https://img.shields.io/badge/SQLite)

---

## 📌 Descripción | Description

Este proyecto automatiza el scraping de portales de empleo, buscando nuevas ofertas de desarrollador Python y actualizando los resultados cada día.

This project automates job board scraping, searching for new offers as Python developer and updating results every day.

Ideal para mantenerte al tanto de oportunidades sin mover un dedo.

Ideal to keep track of job opportunities without lifting a finger.

---

## 🧰 Tecnologías | Technologies

- 🐍 Python 3
- Selenium
- Flask
- SQLite
- BeautifulSoup   


## 🖥️ Cómo ejecutar el proyecto localmente / How to Run the Project Locally

1. **Clonar el repositorio / Clone the Repository:**
   ```bash
   git clone https://github.com/dariomlopez/automation-job-search
   cd tu-repo
   ```

2. **Crea un entorno virtual (opcional pero recomendado)/ Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   ```

3. **Instala las dependencias / Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Actualiza la base de datos lanzando el scraping / Update the database :**
Ejecuta el archivo / execute run_scraper.py:
   ```
   python run_scrapers.py
   ```

4. **Iniciar la web con Flask / Start the web application using Flask:**
Abrir una terminal en en la carpeta donde se encuentra app.py / From the directory containing app.py, run:
Ejecutar:
   ```bash
   flask run
   ```

