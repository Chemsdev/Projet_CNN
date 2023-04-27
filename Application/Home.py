# Import des utilitaires.
import streamlit as st 
from librairie import create_table, print_image
import numpy as np


def main():
    
    # Création de la table.
    create_table(table_name="picture_predict", name_bdd="neuronal_convolutif")
    
    # Accueil (titre & header).
    st.title("Visualisation réseau neuronal convolutif")
    st.header("Accueil")  
    
    # Créer trois colonnes pour aligner les images en largeur.
    col1, col2, col3 = st.columns(3)

    # Pour chaque colonne, on affiche 3 images
    with col1:
        for i in (1,2,3,4):
            print_image(index=i, n_image=i)

    with col2:
        for i in (5,6,7,8):
            print_image(index=i, n_image=i)

    with col3:
        for i in (9,10,11,12):
            print_image(index=i, n_image=i)
            
    st.header("Prédictions...")


main()


