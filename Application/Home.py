# Import des utilitaires.
import streamlit as st 
from bdd import create_table

def main():
    # Création de la table
    create_table(table_name="picture_predict")
    
    # Accueil (titre & header)
    st.header("Outil de visualisation pour un réseau neuronal convolutif")
    st.title("Accueil")     
main()


