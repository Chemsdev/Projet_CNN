# Import des utilitaires.
import streamlit as st 
from bdd import create_table

from modelling import print_picture, x_test

def main():
    
    # Création de la table.
    create_table(table_name="picture_predict", name_bdd="neuronal_convolutif")
    
    # Accueil (titre & header).
    st.header("Outil de visualisation pour un réseau neuronal convolutif")
    st.title("Accueil")  
    
    # Affichage d'une image.
    print_picture()
       
main()


