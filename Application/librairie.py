
# Import des librairies.
from sqlalchemy import create_engine
from sqlalchemy import inspect
import streamlit as st
import numpy as np
import pymysql
import pandas as pd

# Import des utilitaires pour le modèle.
import tensorflow as tf
from tensorflow import keras
from bdd import send_sql_table_2_tables

# =========================== Utilitaires ====================================>

# Import de la data.
x_train = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet/data/train.csv")
x_test  = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet\data/test.csv")

# connexion à la base de données.
conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')

# importation du modèle 
model = tf.keras.models.load_model("C:/Users/Chems Ounissi/Desktop/CNN_projet/my_model2.h5")

# =========================== Les fonctions ====================================>
   
# Fonction : permettent d'afficher une image sur notre site web.
def print_image(index:int, test=x_test):
    style = """
    img {
        border-radius: 5px;
        transition: transform 0s ease-in-out;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5);
    }
    
    img:hover {
        transform: scale(1.1);
    }
    """
    test = np.array(test)
    features  = test[index]
    img  = features.reshape((28, 28))
    st.write(f'<style>{style}</style>', unsafe_allow_html=True)
    st.image(img, width=80)
    return features

# =============================================================================>

# Fonction permettent de placer une image de fond pour site web.
def background(url:str):
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url({url});
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
    )

# =============================================================================>

# Fonction permettent de charger des images en local.
def CSS_picture(predict):
    picture = f"image pred/{predict.item()}.jpg"
    st.write(unsafe_allow_html=False)
    st.image(picture, width=300)

# =============================================================================>

# Fonction permettent d'apporter du CSS à nos pages.
def css_page():
    st.markdown("""
    <style>
        body {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        }
        
        h1 {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            color: #FD942F;
            text-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5);
        }
        
    </style>
    """, unsafe_allow_html=True)

# =============================================================================>

# Fonction permettent d'afficher les images et le résultat de la prédiction.
def column_picture():
    
    # Affichage des images.
    col1, col2, col3 = st.columns(3)
    finish=False
    keep_index=0
    
    with col1:
        for i in (17, 12, 5):
            features = print_image(index=i)     
            keep_index = i       
            if st.button("prédire", key=i):
                pred = execute_model(features=features, model=model)
                finish=True
                
    with col2:
        for i in (0, 10, 44):
            features = print_image(index=i)
            keep_index = i    
            if st.button("prédire", key=i):
                pred = execute_model(features=features, model=model)
                finish=True
    
    with col3:
        for i in (4, 50, 2):
            features = print_image(index=i)   
            keep_index = i             
            if st.button("prédire", key=i):
                pred = execute_model(features=features, model=model)
                finish=True
    
    if finish:
        
        # Affichage du résultat.
        st.title("Prédiction...")
        st.subheader(f"Le modèle à trouver !")
        CSS_picture(predict=pred)
   
        # On envoie les données en BDD.
        send_sql_table_2_tables(
            prediction = pred, 
            index      = keep_index, 
            features   = features, 
            y_true     = "oui"
        )
        
# =============================================================================

# Fonction permettent d'utiliser le modèle.
def execute_model(features, model=model):
    prediction = model.predict(((features).reshape((-1,28,28,1)))/255.0)
    prediction = np.argmax(prediction, axis=1)
    return prediction
