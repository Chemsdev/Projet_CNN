# Import des utilitaires.
import streamlit as st 
from librairie import background, column_picture, css_page
from bdd_2_tables import create_tables_2_tables
import numpy as np

def main():
        
    css_page()
    
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

