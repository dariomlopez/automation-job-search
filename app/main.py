import pandas as pd
import os
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Job Search Results",
    page_icon="📊",
    layout="wide"
)

# Ruta donde se encuentran los resultados
RESULTS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scrapers', 'results')

st.title("📊 Job Search Results")

if not os.path.exists(RESULTS_FOLDER):
    st.error(f"La carpeta de resultados no existe: {RESULTS_FOLDER}")
else:
    csv_files = [f for f in os.listdir(RESULTS_FOLDER) if f.endswith('.csv')]
    
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
                    st.dataframe(
                        df,
                        use_container_width=True,
                        column_config={
                            "url": st.column_config.LinkColumn("URL"),
                            "link": st.column_config.LinkColumn("Link")
                        }
                    )
                    
                    # Botón de descarga
                    st.download_button(
                        "📥 Descargar CSV",
                        df.to_csv(index=False).encode('utf-8'),
                        csv_file,
                        "text/csv"
                    )

            except Exception as e:
                st.error(f"❌ Error al leer {csv_file}: {str(e)}")
