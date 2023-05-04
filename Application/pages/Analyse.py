# Import des librairies.
from librairie import background, css_page
import pymysql
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from bdd import delete_content_tables
from bdd import delete_content_tables

# connexion à la base de données.
conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')


def analyse():
    
    # Apporter du CSS à ma page.
    css_page()
    
    # Titre de la page.
    st.title("Notre base de données")
    st.subheader("Table de prédictions")
    
    # affichage du background.
    background(url="https://wallpaper.dog/large/10707630.jpg")
    
    # ============================================== IMAGE STATS  ============================================== #
     
    # Récupération de la data
    table_images=pd.read_sql_query("SELECT * FROM images ", conn)
    table_predictions=pd.read_sql_query("SELECT * FROM predictions ", conn)
    data=False
    
    # Si la table est vide, on envoie un message d'erreur.
    if table_images.empty or table_predictions.empty:
        st.error("Base de données vide !")
        
    # Sinon, on prépare la data à l'analyse.
    else:
        df_final = table_predictions.merge(table_images, left_on='image_id', right_on='id')
        df_final = df_final.drop(["id_x", "id_y","image_id"], axis=1)
        st.write(df_final.head())
        data=True
        
    # Bouton pour supprimer les données. 
    if st.button("Supprimer les données", key="pred"):
        delete_content_tables(table="pred")
    
    # Si les tables ne sont pas vide, on affiche l'analyse.
    if data:
        
        # Titre de la sous-page.
        st.title("Analyse des Prédictions")
        
        # ========== Graphique 1 (Prédictions)========== #
        st.subheader('Les Prédictions réalisées')
        sns.set_style('dark')
        fig, ax = plt.subplots()  
        sns.countplot(x='y_pred', data=df_final, ax=ax)  
        plt.xlabel("Les cibles prédites")
        plt.ylabel("Compte des cibles prédites")
        plt.savefig('countplot.png')  
        st.image('countplot.png')  
        st.markdown(f"**Vous avez fait {df_final.shape[0]} prédiction(s)** !")
        
        # ========== Graphique 2 (Prédictions) =============== #
        st.subheader('Les Performances du Modèle')
        nb_oui = df_final[df_final["y_true"] == "oui"].shape[0]
        nb_non = df_final[df_final["y_true"] == "non"].shape[0]
        fig, ax = plt.subplots()
        ax.bar(["Bonne prédiction", "Mauvaise prédiction"], [nb_oui, nb_non],  color=["#80ff80", "#ff8080"])
        st.pyplot(fig)
        
        # ============================================== CANVAS STATS  ======================================== #
        st.title('Le modèle avec Canvas')
        
        # Récupération de la data
        table_canvas = pd.read_sql_query("SELECT * FROM canvas ", conn)
        
        # Titre et affichage de la table
        st.subheader("Table Canvas")
        st.write(table_canvas)
            
        # Bouton pour supprimer les données. 
        if st.button("Supprimer les données",  key="canvas"):
            delete_content_tables(table="canvas")
            
        # Vérification de la quantité de la data pour le graphique.
        if table_canvas.empty or table_canvas.shape[0] < 5:
            st.warning("Pas assez de données...")
            
        else:    
            
            # ========== Graphique 1 (canvas) ================ #  
            st.subheader('Les Performances du modèle avec Canvas')              
            nb_oui = table_canvas[table_canvas["y_true"] == "Oui"].shape[0]
            nb_non = table_canvas[table_canvas["y_true"] == "Non"].shape[0]
            fig, ax = plt.subplots()
            ax.bar(["Bonne prédiction", "Mauvaise prédiction"], [nb_oui, nb_non],  color=["#80ff80", "#ff8080"])
            st.pyplot(fig)
            st.markdown(f"**Vous avez fait {table_canvas.shape[0]} prédiction(s)** !")
            
            # ========== Graphique 2 (Canvas)========== #
            st.subheader('Les Prédictions réalisées')
            sns.set_style('dark')
            fig, ax = plt.subplots()  
            sns.countplot(x='y_pred', data=table_canvas, ax=ax)  
            plt.xlabel("Les cibles prédites")
            plt.ylabel("Compte des cibles prédites")
            plt.savefig('countplot.png')  
            st.image('countplot.png')  
            st.markdown(f"**Vous avez fait {table_canvas.shape[0]} prédiction(s)** !")

    # Sinon on renvoie un message d'erreur.
    else:
        st.error("Visualisation non disponible.")
        
analyse()


