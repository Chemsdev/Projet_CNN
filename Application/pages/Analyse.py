# Import des librairies.
from librairie import background, css_page
import pymysql
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from bdd_2_tables import delete_content_tables

# connexion à la base de données.
conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')


def analyse():
    
    css_page()
    
    # Titre de la page.
    st.title("Notre base de données")
    st.subheader("Table de prédictions")
    
    # affichage du background + connexion à la base.
    background(url="https://wallpaper.dog/large/10707630.jpg")
    table_images=pd.read_sql_query("SELECT * FROM images ", conn)
    table_predictions=pd.read_sql_query("SELECT * FROM predictions ", conn)
    data=False
    
    # Si la table est vide, on envoie un message d'erreur.
    if table_images.empty or  table_predictions.empty:
        st.error("Base de données vide !")
        
    # Sinon, on prépare la data à l'analyse.
    else:
        df_final = table_predictions.merge(table_images, left_on='image_id', right_on='id')
        df_final = df_final.drop(["id_x", "id_y","image_id"], axis=1)
        st.write(df_final.head())
        data=True
        
    # Bouton pour supprimer les données. 
    if st.button("Supprimer les données"):
        delete_content_tables()
    
    # Si les tables ne sont pas vide, on affiche l'analyse.
    if data:
        
        # Titre de la sous-page.
        st.title(f"Analyse des Prédictions")
        
        # ========== Graphique 1 ========== #
        st.subheader('Les Prédictions réaliser')
        sns.set_style('dark')
        fig, ax = plt.subplots()  
        sns.countplot(x='y_pred', data=df_final, ax=ax)  
        plt.xlabel("Les cibles prédites")
        plt.ylabel("Compte des cibles prédites")
        fig.savefig('countplot.png')  
        st.image('countplot.png')  
        st.markdown(f"**Vous avez fait {df_final.shape[0]} prédictions(s)** !")
        
    # Sinon on renvoie un message d'erreur.
    else:
        st.error("Visualisation non disponible.")
        
analyse()


