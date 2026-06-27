
import sys
import streamlit as st
import geopandas as gpd
from shapely.geometry import Polygon

class ROI():
    def __init__(self, crosswalks):
        self.crosswalks=crosswalks
        self.gdf=None
        self.squares = []
        self.points= []


    def create_square(self):
        try:
            if self.crosswalks['elements']!=[]:
                #center point extraction
                self.points = [(point['lat'], point['lon']) for point in self.crosswalks['elements']]

                #creating rectangles
                for i in self.points:
                    if st.session_state['status']:
                        sys.exit(0)

                    lat, lon = i  # Central point
                    side_length = 0.00006  # Length of the side of the square in degrees
                    half_side = side_length
                    sw = (lon - half_side, lat - half_side)  # Point SW
                    se = (lon + half_side, lat - half_side)  # Point SE
                    ne = (lon + half_side, lat + half_side)  # Point NE
                    nw = (lon - half_side, lat + half_side)  # Point NW
                    rectangle = Polygon([sw, se, ne, nw])
                    self.squares.append(rectangle)

                #Create a GeoDataframe
                self.gdf = gpd.GeoDataFrame(geometry=self.squares, crs='epsg:4326')
                return self.points
        except:
            pass


