import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import time
import locale

from scrapers import general_job_search, scrape_ticjob, scrape_infojobs, scrape_indeed

# Ruta donde se guardan los resultados
RESULTS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scrapers', 'results')
ESTIMATED_TOTAL_TIME = 60

print("DEFAULT ENCODING:", locale.getpreferredencoding())

host = os.getenv("STREAMLIT_HOST", "localhost")
port = os.getenv("STREAMLIT_PORT", "8501")

url = f"http://{host}:{port}"
print(f"\n[Streamlit] La app se está ejecutando en: {url}\n")

st.title("Job Search Automation")

def run_all_scrapers():
    info_container = st.empty()
    info_container.info("Scraping executing, please wait... This may take a while.")
    try:
        general_job_search()
        scrape_indeed()
        scrape_ticjob()
        scrape_infojobs()
        info_container.empty()
        st.success("Scraping completed.")
        st.session_state.scraping_done = True
    except Exception as e:
        info_container.empty()
        st.error(f"Error while scraping: {e}")
        st.stop()

if 'scraping_done' not in st.session_state:
    run_all_scrapers()

if st.button("🔁 Execute scraping again"):
    run_all_scrapers()

if not os.path.exists(RESULTS_FOLDER):
    st.error(f"La carpeta de resultados no existe: {RESULTS_FOLDER}")
else:
    csv_files = [f for f in os.listdir(RESULTS_FOLDER) if f.endswith('.csv')]
    if not csv_files:
        st.warning("No hay archivos CSV disponibles para mostrar.")
    else:
        for csv_file in csv_files:
            file_path = os.path.join(RESULTS_FOLDER, csv_file)
            try:
                df = pd.read_csv(file_path)
                if df.empty:
                    st.info(f"ℹ️ El archivo `{csv_file}` está vacío.")
                    continue

                st.subheader(f"📄 Resultados en `{csv_file}`")
                df_display = df.copy()

                # Asegurarse de que el nombre de columna con los links es correcto
                link_col = 'url' if 'url' in df.columns else 'link' if 'link' in df.columns else None

                if link_col:
                    df_display[link_col] = df_display[link_col].apply(
                        lambda x: f'<a href="{x}" target="_blank">{x}</a>' if pd.notna(x) else x
                    )
                    st.markdown(
                        df_display.to_html(escape=False, index=False),
                        unsafe_allow_html=True
                    )
                else:
                    st.dataframe(df_display)

            except pd.errors.EmptyDataError:
                st.warning(f"ℹ️ El archivo `{csv_file}` está vacío.")
            except Exception as e:
                st.error(f"❌ No se pudo leer `{csv_file}`: {e}")
