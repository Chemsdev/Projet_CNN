# Import des utilitaires.
import streamlit as st 
from librairie import create_table, background, column_picture
import numpy as np
import random
from PIL import Image
import base64
import secrets




def main():
        
    # Définir l'image de fond
    st.markdown("""
    <style>
        body {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # background de notre site web.
    background(url="https://wallpaper.dog/large/10707630.jpg")
    
    # Création de la table.
    create_table(table_name="picture_predict", name_bdd="neuronal_convolutif")
    
    # Accueil (titre & header).
    st.title("Réseau neuronal Convolutif")
    st.header("Accueil")  
    
    # message pour l'utilisteur
    st.markdown('**Veuillez choisir une image...**')
    
    # Affichage des images
    column_picture()


main()

