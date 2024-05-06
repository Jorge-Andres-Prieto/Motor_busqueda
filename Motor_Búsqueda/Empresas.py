import streamlit as st  # Importa Streamlit para construir interfaces de usuario
import pandas as pd  # Importa Pandas para manejar estructuras de datos
from streamlit_lottie import st_lottie  # Importa st_lottie para mostrar animaciones
import requests  # Importa requests para realizar solicitudes HTTP


class SearchApp:
    """Define una aplicación de búsqueda con funcionalidades específicas.

    Args:
        None

    Returns:
        None

    """

    def __init__(self):
        """
        Inicializa la aplicación con configuraciones predeterminadas, incluyendo
        las URL para cargar una animación Lottie y los datos desde Google Sheets.

        Args:
        None

        Returns:
        None

        """
        self.lottie_url = ('https://raw.githubusercontent.com/Jorge-Andres-Prieto/Motor_busqueda/main/'
                           '.streamlit/assets/Animation%20-%201713681616801.json')
        self.data_url = ('https://docs.google.com/spreadsheets/d/e/2PACX-1vR9IGQhDWN0qA-jon8x0'
                         'cUTap8IxvrdzGjF_kN98upNSQDeDJsI6UkpyGYOtPV18cbSB-rQzU62btO6/pub?'
                         'gid=446676900&single=true&output=csv')

    def load_lottiefile(self, url: str) -> dict:
        """
        Carga un archivo Lottie JSON desde una URL.

        Args:
            url: La URL del archivo Lottie JSON a cargar.

        Returns:
            Un diccionario que representa el archivo Lottie JSON cargado o un
            diccionario vacío si hay un error.
        """
        try:
            r = requests.get(url)
            r.raise_for_status()  # Esto lanzará un error si el estado HTTP no es 200
            return r.json()
        except requests.RequestException as e:
            print(f"Error al cargar Lottie JSON desde la URL: {url}")
            print(str(e))
            return {}
        except requests.exceptions.JSONDecodeError:
            print("No se pudo decodificar JSON en la respuesta.")
            print(r.text)  # Imprimirá la respuesta para ayudar a diagnosticar el problema
            return {}

    def load_data(self) -> pd.DataFrame:
        """
        Carga los datos desde una URL predefinida y los devuelve como un DataFrame.

        Returns:
            Un DataFrame con los datos cargados desde una URL predefinida.

        Args:
        None

        Returns:
        None

        """
        return pd.read_csv(self.data_url)

    def main(self):
        """Ejecuta la aplicación principal y muestra los componentes de UI.

        Args:
        None

        Returns:
        None

        """
        st.markdown("<h1 style='text-align: center; color: white;'>Motor de Búsqueda</h1>", unsafe_allow_html=True)
        self.display_lottie_animation()
        registradas_df = self.load_data()

        termino_busqueda = st.text_input("Ingrese el nombre de la empresa a buscar:", "")
        if st.button("Buscar"):
            self.search_and_display_results(registradas_df, termino_busqueda)

    def display_lottie_animation(self):
        """
        Muestra una animación Lottie centrada en la pantalla.

        Returns:
            None. La función solo muestra una animación en la UI.

        Args:
        None

        Returns:
        None

        """
        lottie_animation = self.load_lottiefile(self.lottie_url)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if lottie_animation:
                st_lottie(lottie_animation, speed=1, height=150, width=280, key="initial")

    def search_and_display_results(self, df: pd.DataFrame, search_term: str):
        """
        Busca un término específico en el DataFrame y muestra los resultados.

        Args:
            df: DataFrame donde se realizará la búsqueda.
            search_term: El término de búsqueda ingresado por el usuario.

        Returns:
            None. Los resultados se muestran directamente en la UI.
        """
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
