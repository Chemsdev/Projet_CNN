
# Import des librairies
from librairie import background
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from tensorflow import keras
import cv2
import tensorflow as tf
import numpy as np

# Import des librairies.
import streamlit as st
import numpy as np
import pymysql
import pandas as pd

# =========================== Utilitaires =======================================>

# Import de la data.
x_train = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet/data/train.csv")
x_test  = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet\data/test.csv")

# connexion à la base de données.
conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')

# importation du modèle 
model = tf.keras.models.load_model("C:/Users/Chems Ounissi/Desktop/CNN_projet/my_model2.h5")


def canvas(x_test=x_test, model=model):
    background(url="https://wallpaper.dog/large/10707630.jpg")
    st.title("Draw your number here")


    canvas_result = st_canvas(
        height=300,width=400,
        fill_color='#ffffff', background_color='#000000',
        stroke_width=10,
        stroke_color='#ffffff',
        drawing_mode='freedraw',
        key='canvas')

    if canvas_result.image_data is not None :
        img = cv2.resize(canvas_result.image_data.astype('uint8'),(28,28))
    
    if st.button('predict') :
        x_test = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        pred = model.predict((x_test.reshape(-1,28,28,1))/255)
        st.write(f'result: {np.argmax(pred[0])}')
              
canvas()

