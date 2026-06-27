
import cv2
import base64
import folium
import pandas as pd
from folium import plugins
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster


class layout:
    def __init__(self, geometry=None):
        self.geometry=geometry


    def get_map(self):
        m=folium.Map(location=[39.469709, -0.375054], zoom_start=12, max_bounds=True, min_lat=37.4344, max_lat=41.0951, min_lon=-1.8688, max_lon=1.04411)

        try:
            if isinstance(self.geometry, pd.DataFrame) and not self.geometry.empty:
                marker_cluster = MarkerCluster(name='Pasos peatonales').add_to(m)

                for idx, row in self.geometry.iterrows():
                    if row['predict'] == 0:#Clase bien
                        #make Marker
                        imagen = cv2.imread(row['path'])
                        imagen = cv2.resize(imagen, (125, 163))
                        retval, buffer = cv2.imencode('.jpeg', imagen)
                        imagen_base64 = base64.b64encode(buffer).decode('utf-8')
                        additional_text = f'<p style="text-align: center; color: green; font-weight: bold;">En buen estado</p>'
                        popup_html = f'<div>{additional_text} <img src="data:image/jpeg;base64,{imagen_base64}"></div>'
                        popup = folium.Popup(html=popup_html, max_width=400)
                        peatonal_icon = folium.CustomIcon(icon_image='data/icon/icon_bien.png', icon_size=(20, 20))
                        folium.Marker(row['coords'], popup=popup, icon=peatonal_icon).add_to(marker_cluster)


                    elif row['predict'] == 1:
                        #make Marker
                        imagen = cv2.imread(row['path'])
                        imagen = cv2.resize(imagen, (125, 163))
                        retval, buffer = cv2.imencode('.jpeg', imagen)
                        imagen_base64 = base64.b64encode(buffer).decode('utf-8')
                        additional_text = f'<p style="text-align: center; color: red; font-weight: bold;"> En mal estado </p>'
                        popup_html = f'<div>{additional_text} <img src="data:image/jpeg;base64,{imagen_base64}"></div>'
                        popup = folium.Popup(html=popup_html, max_width=400, )
                        peatonal_icon = folium.CustomIcon(icon_image='data/icon/icon_mal.png', icon_size=(25, 25))
                        folium.Marker(row['coords'], popup=popup, icon=peatonal_icon).add_to(marker_cluster)

                m.add_child(marker_cluster)
        except:
            pass


        # WMS ICV-2022
        folium.raster_layers.WmsTileLayer(url = 'https://terramapas.icv.gva.es/0202_2022CVAL0025?',
                                          layers = '2022CVAL0025_RGB',
                                          fmt ='image/png',
                                          transparent = True,
                                          control = True,
                                          name = 'Imagen aérea-2022',
                                          overlay=True,
                                          show = True).add_to(m)
        folium.LayerControl().add_to(m)

        # Draw control
        style={'color': '#ff0000', 'fillColor': '#ffff00', 'fillOpacity': 0.3}
        draw_control = plugins.Draw(show_geometry_on_click=False, position='topleft',
                                    draw_options={'rectangle':{'shapeOptions': style}, 'polygon':False,
                                                  'marker': False, 'polyline':False, 'circleMarker':False,'circle':False,
                                                  'circlemarker':False,'CircleMarker':False})
        m.add_child(draw_control)

        render_m= st_folium(m, key='map', width='100%', height=750)
        coordinates=[]
        try:
            if render_m['last_active_drawing']:
                lat_min=render_m['last_active_drawing']['geometry']['coordinates'][0][0][1]
                lon_min=render_m['last_active_drawing']['geometry']['coordinates'][0][0][0]
                lat_max=render_m['last_active_drawing']['geometry']['coordinates'][0][2][1]
                lon_max=render_m['last_active_drawing']['geometry']['coordinates'][0][2][0]
                coordinates=[lat_min, lon_min, lat_max, lon_max]
        except:
            pass

        return (m,coordinates)




