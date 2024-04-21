import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import requests  # Importar requests para cargar archivos desde URL

class SearchApp:
    def __init__(self):
        """Inicializa la aplicación con configuraciones predeterminadas."""
        # URL directa a la versión raw de tu archivo Lottie en GitHub
        self.lottie_url = "https://raw.githubusercontent.com/Jorge-Andres-Prieto/ppi_pl_PRIETOj/main/Motor_B%C3%BAsqueda/.streamlit/assets/Animation%20-%201713681616801.json"
        self.data_url = ('https://docs.google.com/spreadsheets/d/e/2PACX-1vR9IGQhDWN0qA-jon8x0'
                         'cUTap8IxvrdzGjF_kN98upNSQDeDJsI6UkpyGYOtPV18cbSB-rQzU62btO6/pub?'
                         'gid=446676900&single=true&output=csv')

    def load_lottiefile(self, url: str) -> dict:
        """Carga un archivo Lottie JSON desde una URL."""
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            return {}  # Retorna un diccionario vacío si hay error

    def load_data(self) -> pd.DataFrame:
        """Carga los datos desde una URL predefinida."""
        return pd.read_csv(self.data_url)

    def main(self):
        """Ejecuta la aplicación principal."""
        st.markdown("<h1 style='text-align: center; color: white;'>Motor de Búsqueda</h1>", unsafe_allow_html=True)
        self.display_lottie_animation()
        registradas_df = self.load_data()

        termino_busqueda = st.text_input("Ingrese el nombre de la empresa a buscar:", "")
        if st.button("Buscar"):
            self.search_and_display_results(registradas_df, termino_busqueda)

    def display_lottie_animation(self):
        """Muestra una animación Lottie centrada en la pantalla."""
        lottie_animation = self.load_lottiefile(self.lottie_url)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if lottie_animation:
                st_lottie(lottie_animation, speed=1, height=150, width=280, key="initial")

    def search_and_display_results(self, df: pd.DataFrame, search_term: str):
        """Busca en el DataFrame y muestra los resultados."""
        if search_term:
            search_term = search_term.upper().strip()
            results_df = df[df["RAZON SOCIAL"].str.contains(search_term, case=False, na=False)]
            if len(results_df) > 0:
                st.table(results_df)
            else:
                st.error("No se encontraron empresas con el nombre ingresado.")
        else:
            st.warning("Por favor, ingrese un término de búsqueda.")

if __name__ == "__main__":
    app = SearchApp()
    app.main()
