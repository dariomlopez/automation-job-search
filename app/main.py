import pandas as pd
import os
import streamlit as st
import datetime

today = datetime.date.today()

# Configuración de la página
st.set_page_config(
    page_title="Job Search Results",
    page_icon="📊",
    layout="wide"
)

# Ruta donde se encuentran los resultados
RESULTS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scrapers', 'results')

st.title("📊 Job Search Results")

def make_links_clickable(df, col_names):
    """Convierte columnas con URLs en links clicables en HTML."""
    for col in col_names:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: f'<a href="{x}" target="_blank">{x}</a>' if pd.notna(x) and x != "" else ""
            )
    return df

if not os.path.exists(RESULTS_FOLDER):
    st.error(f"La carpeta de resultados no existe: {RESULTS_FOLDER}")
    os.makedirs(RESULTS_FOLDER)
    st.info(f"Se ha creado la carpeta de resultados: {RESULTS_FOLDER}")
else:
    csv_files = [f for f in os.listdir(RESULTS_FOLDER) if f.endswith('.csv')]
    
    # Filtrar archivos por fecha de modificación (solo los de hoy)
    csv_files = [
        f for f in csv_files if datetime.date.fromtimestamp(os.path.getmtime(os.path.join(RESULTS_FOLDER, f))) == today
    ]

    if not csv_files:
        st.warning("No hay archivos CSV disponibles.")
    else:
        for csv_file in csv_files:
            file_path = os.path.join(RESULTS_FOLDER, csv_file)
            try:
                df = pd.read_csv(file_path)
                if df.empty:
                    st.info(f"ℹ️ El archivo `{csv_file}` está vacío.")
                    continue

                with st.expander(f"📄 {csv_file}", expanded=True):
                    # Crear copia y convertir links a HTML clicable
                    df_display = make_links_clickable(df.copy(), ['url', 'link'])

                    # Mostrar tabla con links clicables
                    st.markdown(
                        df_display.to_html(escape=False, index=False),
                        unsafe_allow_html=True
                    )
                    
                    # Botón para descargar CSV
                    st.download_button(
                        "📥 Descargar CSV",
                        df.to_csv(index=False).encode('utf-8'),
                        csv_file,
                        "text/csv"
                    )

            except Exception as e:
                st.error(f"❌ Error al leer {csv_file}: {str(e)}")
