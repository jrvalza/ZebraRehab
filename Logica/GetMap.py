
import sys
import requests
import streamlit as st
from pyproj import CRS
import geopandas as gpd
from Logica.folders import folder_management

class WMS():
    def __init__(self, gdf=None):
        self.gdf=gdf


    def request_GetMap(self):

        #dir path to save
        output_shapefile = "data/to_predict/"
        folder_output=folder_management(output_shapefile).folder()

        try:
            #download images
            if isinstance(self.gdf, gpd.GeoDataFrame) and not self.gdf.empty:
                utm30 = CRS.from_epsg(25830)
                self.gdf = self.gdf.to_crs(utm30)
                width = 500
                for i, geom in enumerate(self.gdf.geometry):

                    if st.session_state['status']:
                        folder_output
                        sys.exit(0)

                    minx = geom.bounds[0]
                    miny = geom.bounds[1]
                    maxx = geom.bounds[2]
                    maxy = geom.bounds[3]
                    wms = 'https://terramapas.icv.gva.es/0202_2022CVAL0025?'
                    request = 'request=GetMap&service=WMS&version=1.3.0&'
                    layer = 'layers=2022CVAL0025_RGB&'
                    sys_ref = f'CRS=EPSG:{self.gdf.crs.to_epsg()}&'
                    region = f'BBOX={minx},{miny},{maxx},{maxy}&'

                    height = int(round(width/((maxx-minx)/(maxy-miny)),0))
                    image = f'Width={width}&height={height}&format=image/jpeg'
                    getmap = wms+request+layer+sys_ref+region+image

                    #GetMap
                    response = requests.get(getmap)

                    if response.status_code == 200:
                        # image in bytes
                        image = response.content

                        # save images in jpeg format
                        file = f'data/to_predict/image_{i}.jpeg'
                        with open(file, 'wb') as file:
                            file.write(response.content)
        except:
            pass


