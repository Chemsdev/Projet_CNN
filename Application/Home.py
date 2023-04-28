# Import des utilitaires.
import streamlit as st 
from librairie import create_table, print_image, send_sql_table
import numpy as np
import random
from PIL import Image
import base64


def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://wallpaper.dog/large/10707630.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def main():
    
    add_bg_from_url()
    
    
    # Définir l'image de fond
    st.markdown("""
    <style>
        body {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    """,unsafe_allow_html=True)
    
    add_bg_from_url() 
    
    # Création de la table.
    create_table(table_name="picture_predict", name_bdd="neuronal_convolutif")
    
    # Accueil (titre & header).
    st.title("Visualisation réseau neuronal convolutif")
    st.header("Accueil")  
    
    # message pour l'utilisteur
    st.markdown('**Veuillez choisir une image...**')
    
    # Affichage des images, enregistrement de l'image en BDD, prédiction.
    col1, col2, col3 = st.columns(3)
    finish = False
    
    with col1:
        for i in range(1, 4):
            print_image(index=i)
            if st.button('prédire', key=f'image_{i}'):
                pred = send_sql_table(index=i)
                finish = True
                
    with col2:
        for i in range(4, 7):
            print_image(index=i)
            if st.button('prédire', key=f'image_{i}'):
                pred = send_sql_table(index=i)
                finish = True
                
    with col3:
        for i in range(7, 10):
            print_image(index=i)
            if st.button('prédire', key=f'image_{i}'):
                pred = send_sql_table(index=i)
                finish = True
        
    if finish :
        st.header("Prédiction")
        st.markdown(f"**Résultat de la prédiction : {pred.item()}**")
    



main()

