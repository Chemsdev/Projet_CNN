# Import des librairies.
from librairie import background
import pymysql
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from librairie import delete_table

# connexion à la base de données.
conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')


def page_bdd():
    
    st.title("Notre base de données")
    st.header("Table de prédictions")
    
    # affichage du background + connexion à la base
    background(url="https://wallpaper.dog/large/10707630.jpg")
    table_images=pd.read_sql_query("SELECT * FROM images ", conn)
    table_predictions=pd.read_sql_query("SELECT * FROM predictions ", conn)
    data=False
    
    # Si la table est vide, on envoie un message d'erreur.
    if table_images.empty or  table_predictions.empty:
        st.error("Base de données vide !")
    else:
        df_joined = table_predictions.merge(table_images, left_on='image_id', right_on='id')
        df_joined = df_joined.drop(["id_x", "id_y"], axis=1)
        st.write(df_joined.head())
        data=True
    
    # Affichage du nombre d'occurrences de chaque valeur
    st.header(f"Exploration des Prédictions")
    if data:
        sns.set_style('dark')
        fig = sns.countplot(x='y_pred', data=df_joined)
        fig = fig.get_figure()  
        fig.savefig('countplot.png')  
        st.image('countplot.png')  
    else:
        st.error("Visualisation non disponible.")
        
page_bdd()


