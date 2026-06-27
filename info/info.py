
import streamlit as st

#Sidebar
def info ():

    st.markdown("<header style='text-align: center; color: white; font-size: 60px'>🦓</header>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white;'>ZebraRehab</h1>", unsafe_allow_html=True)

    st.header("Información")
    st.info("ZebraRehab es una aplicación diseñada para ayudar a mejorar la seguridad vial y la infraestructura peatonal.")

    st.header("Cómo usar")
    st.info("1. Seleccione una zona de búsqueda con el control rectangular de dibujo.")
    st.info("2. Haz clic en el botón 'Detectar' para que la aplicación analice las imágenes.")
    st.info("3. Espera unos segundos para obtener los resultados de la detección.")
    st.info("4. La aplicación mostrará si el paso peatonal se encuentra en buen estado o mal estado.")
    image1_path = "data/icon/icon_bien.png"
    image2_path = "data/icon/icon_mal.png"

    col1, col2 = st.columns(2)
    with col1:
        st.image(image1_path, caption="buen estado", use_column_width=True)
    with col2:
        st.image(image2_path, caption="mal estado", use_column_width=True)

    st.header("¿Cómo funciona?:")
    st.info("- Geolocalización de pasos peatonales consultando la API Overpass de OpenStreetMap.")
    st.info("- Obtención de imágenes mediante peticiones GetMap al WMS del Plan Nacional de Ortofotografía Aérea.")
    st.info("- Clasificación del estado de los pasos peatonales en 'buen estado' o 'mal estado mediante Red Neuronal Convolucional previamente entrenada.")

    st.header("Requisitos")
    st.info("Para utilizar ZebraHab, asegúrate de cumplir con los siguientes requisitos:")
    st.info("- Navegador web moderno (Chrome, Firefox, Safari, Edge, etc.).")
