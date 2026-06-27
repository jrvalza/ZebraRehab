import re
import os
import cv2
import keras
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageEnhance



class Predict():
    def __init__(self, points=None):
        self.df = pd.DataFrame()
        self.points=points

    def  make_predictions(self):
        self.df['path']=None
        self.df['predict']=None
        self.df['coords']=None
        model= keras.models.load_model('data/model/CNN.h5')
        folder = "data/to_predict"
        files= os.listdir(folder)

        # read images
        try:
            if not st.session_state['status']:
                for img in files:
                    path_image = os.path.join(folder, img)
                    #get coordinates
                    num = int(re.search(r'image_(\d+)\.jpeg', path_image).group(1))
                    coords=self.points[num]

                    imagen = cv2.imread(path_image)
                    imagen = cv2.resize(imagen, (250, 250))  #resize image to 250x250

                    # Preprocessing
                    eq_b, eq_g, eq_r = cv2.split(imagen)
                    eq_b = cv2.equalizeHist(eq_b)
                    eq_g = cv2.equalizeHist(eq_g)
                    eq_r = cv2.equalizeHist(eq_r)
                    imagen_equalizada = cv2.merge((eq_b, eq_g, eq_r))

                    # Brightness, contrast and edge enhancement
                    brillo=0.2
                    contraste=4.0
                    bordes=10.0
                    imagen_PIL = Image.fromarray(cv2.cvtColor(imagen_equalizada, cv2.COLOR_BGR2RGB))

                    #Brightness
                    enhancer = ImageEnhance.Brightness(imagen_PIL)
                    imagen = enhancer.enhance(brillo)

                    #contrast
                    enhancer = ImageEnhance.Contrast(imagen)
                    imagen = enhancer.enhance(contraste)

                    #edge
                    enhancer = ImageEnhance.Sharpness(imagen)
                    imagen = enhancer.enhance(bordes)

                    # image to luminance conversion and rescaling of pixel values
                    imagen = imagen.convert('L')
                    imagen= np.array([np.array(imagen) / 255.0])

                    # prediction
                    pred = model.predict(imagen)
                    pred = np.round(pred).astype(int)
                    self.df.loc[len(self.df)] = pd.Series({'path': path_image, 'predict': pred[0][0],'coords': list(coords)})
                return self.df

        except:
            pass









