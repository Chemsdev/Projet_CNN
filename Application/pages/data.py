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
    table=pd.read_sql_query("SELECT * FROM picture_predict ", conn)
    data=False
    
    # Si la table est vide, on envoie un message d'erreur.
    if table.empty:
        st.error("Base de données vide !")
    else:
        st.write(table.head())
        data=True
    
    # Dimensions de notre Table.
    st.markdown(f'**Dimensions de la table : { table.shape }**') 
    
    # supressionn de la table
    if st.button("Supprimer les données"):
        delete_table()

    # Affichage du nombre d'occurrences de chaque valeur
    st.header(f"Exploration des Prédictions")

    # On affiche les graphpiques ou on renvoit l'utilisateur à la page prédiction.
    if data:
        sns.set_style('dark')
        fig = sns.countplot(x='label', data=table)
        fig = fig.get_figure()  
        fig.savefig('countplot.png')  
        st.image('countplot.png')  
    else:
        st.error("Visualisation non disponible.")
        
page_bdd()

