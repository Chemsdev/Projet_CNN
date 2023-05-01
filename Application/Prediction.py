# Import des utilitaires.
import streamlit as st 
from librairie import background, column_picture
from bdd_2_tables import create_tables_2_tables
import numpy as np

def main():
        
    # Définition l'image de fond.
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
    
    # background de notre site web.
    background(url="https://wallpaper.dog/large/10707630.jpg")
    
    # Création des 2 tables.
    create_tables_2_tables(name_bdd="neuronal_convolutif")

    # Accueil (titre & header).
    st.title("Réseau neuronal Convolutif")
    
    # message pour l'utilisteur
    st.subheader('**Choissisez une image pour tester !**')
    st.subheader("")
    
    # Affichage des images
    column_picture()

main()

