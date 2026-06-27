
import base64
import pandas as pd
import altair as alt
import streamlit as st
from info.info import info
from Logica.ROIs import ROI
from Logica.GetMap import WMS
from Logica.map import layout
from Logica.OSM import Api_osm
from Logica.predict import Predict
from Logica.folders import folder_management



# Delete images downloaded
def delete_data():
    folder_management('data/to_predict/').folder()

# Background image
def add_bg_from_local(image_file):

    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""<style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
        opacity:0.9;
    }}

    .css-19rxjzo {{color: white;
    background-color: rgba(0,0,0,0.6)}}

    .css-10trblm {{color: white;
    background-color: rgba(0,0,0,0.6);
    border-radius: 100px}}

    .st-ae {{color: white;
    background-color: rgba(0,0,0,0.6);
    border-radius: 20px}}

    .stSpinner{{color: white;
    background-color: rgba(0,0,0,0.6);
    border-radius: 10px}}

    </style>""",unsafe_allow_html=True)

#botton
def handle_click(new_state):
    st.session_state.type=new_state

#map
def map(geometry):
    mapa=layout(geometry)
    return mapa


if __name__ == "__main__":
    #empty folder
    #delete_data()

    # Page config
    st.set_page_config(
    page_title="ZebraRehab",
    page_icon="🦓",
    layout="wide",
    initial_sidebar_state="expanded")

    #Title
    st.markdown("""<div style="text-align: center;"><h1 style="color: white; font-size: 60px; font-family: Roboto, sans-serif"> ZebraRehab</h1></div>""",unsafe_allow_html=True)

    # Background image
    add_bg_from_local('data/icon/bg2.jpeg')

    # Abstract app
    with st.sidebar:
        info()

    # var session state
    if 'mapa' not in st.session_state:
        st.session_state['mapa']=map(None)

    if 'type' not in st.session_state:
        st.session_state['type']='mapa inicial'

    if 'coords' not in st.session_state:
        st.session_state['coords']=None

    if 'points' not in st.session_state:
        st.session_state['points']=None

    if 'df' not in st.session_state:
        st.session_state['df']=None

    if 'status' not in st.session_state:
        st.session_state['status']=False


    #Layout
    pad1, col1, pad2, col2, pad3=st.columns([0.1,15,0.1,2,0.5])

    with col1:
        coords=st.session_state['mapa'].get_map()[1]
        st.session_state['coords'] = coords

    with col2:
        stop=st.button('Reiniciar')
        if stop:
            st.session_state['status']=True
            delete_data()
            st.cache_data.clear()
            st.experimental_rerun()
        else:
            st.session_state['status']=False



        detect=st.button('Detectar')
        if detect:
            with st.spinner("Loading..."):

                #Center points
                Overpass = Api_osm(st.session_state['coords']) # requests OpenStreetMap
                crosswalks = Overpass.get_crosswalks()

                #Delimitation of crosswalks
                ROIs = ROI(crosswalks)
                st.session_state['points'] = ROIs.create_square()

                #download images
                images=WMS(ROIs.gdf)
                images.request_GetMap()

                #predict
                predict=Predict(st.session_state['points'])
                st.session_state['df']=predict.make_predictions()

    with col1:
            #Paint center points
            try:
                if st.session_state['points'] == None or st.session_state['points']==[]:
                    col2.warning("No se han geolocalizado pasos peatonales.", icon="⚠️")

                if isinstance(st.session_state['points'], list):
                    st.session_state['mapa']=map(st.session_state['df'])
                    st.session_state['mapa'].get_map()
                    col2.success("Done!")

            except:
                col2.warning("Seleccione zona de búsqueda", icon="⚠️")

    with col2:
        try:
            if isinstance(st.session_state['df'], pd.DataFrame) and not st.session_state['df'].empty:
                df=st.session_state['df']
                df_0 = df[df['predict'] == 0]
                df_1 = df[df['predict'] == 1]
                bien=(df_0['predict'].count()/df['predict'].count())*100
                mal=(df_1['predict'].count()/df['predict'].count())*100

                data = pd.DataFrame({
                    'Estado': ['bien', 'mal'],
                    'Porcentaje': [bien, mal]})

                # Crear el gráfico utilizando Altair
                c = alt.Chart(data).mark_bar().encode(
                    y='Porcentaje',
                    color='Estado')
                st.markdown("""<div style="text-align: center;"><h4 style="color: white; font-size: 15px; font-family: Roboto, sans-serif"> Distribución</h4></div>""",unsafe_allow_html=True)

                st.altair_chart(c, theme=None, use_container_width=True)


        except:
            pass





