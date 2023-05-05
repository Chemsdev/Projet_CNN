
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
import matplotlib.pyplot as plt
from librairie import css_page, execute_model, CSS_picture
import random

# =========================== Utilitaires =======================================>

# Import de la data.
x_train = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet/data/train.csv")
x_test  = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet\data/test.csv")

# connexion à la base de données.
conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')

# importation du modèle 
model = tf.keras.models.load_model("C:/Users/Chems Ounissi/Desktop/CNN_projet/my_model2.h5")
performances=[]

# =============================================================================>

# Fonction permettent d'insérer des données dans la table canvas.
def bdd_canvas(y_pred, y_true):
    
    # connexion à la bdd.
    conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')
    cursor = conn.cursor()
    
    # On génère code id unique.
    code_id = "".join([str(random.randint(0, 10)) for _ in range(3)]) 
     
    # Préparation des données à l'envoie.
    columns_table =  [ "id",      "y_true",      "y_pred"]
    if int(y_true) == int(y_pred.item()):
        values_table  =  [code_id,     "Oui",        y_pred.item()]  
    else:
        values_table  =  [code_id,     "Non",        y_pred.item()]  

    # Insertion des résultats dans la table predictions.
    sql = f"INSERT INTO canvas ({', '.join(columns_table)}) VALUES ({', '.join(['%s' for i in range(3)])})"
    cursor.execute(sql, values_table)
    
    # Fermeture de la connexion.
    conn.commit()
    conn.close()
    
# =============================================================================>

def canvas(x_test=x_test, model=model):
    
    # Mise en place du CSS
    background(url="https://wallpaper.dog/large/10707630.jpg")
    css_page()
    
    # Accueil (titre et message)
    st.title("Dessine un chiffre !")
    
    options=[0,1,2,3,4,5,6,7,8,9]
    y_true = st.selectbox("Veuillez sélectionner le chiffre que vous allez dessiner.", options)
        
    # Mise en place du canvas
    canvas_result = st_canvas(
        height=300,width=400,
        fill_color='#ffffff', background_color='#000000',
        stroke_width=10,
        stroke_color='#ffffff',
        drawing_mode='freedraw',
        key="canvas")

    if canvas_result.image_data is not None :
        img = cv2.resize(canvas_result.image_data.astype('uint8'),(28,28))
    
    # Action du bouton prédire
    if st.button('prédire') :
        
        # Lancement de la prédiction.
        x_test = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        pred = execute_model(features=x_test, model=model)

        # Affiche du résultat de la prédiction.
        st.title("Prédiction...")
        st.subheader(f"Le modèle à trouver !")
        CSS_picture(predict=pred)
        bdd_canvas(y_pred=pred, y_true=y_true)
    
canvas()

