# Import des utilitaires.
import streamlit as st 
from librairie import create_table, print_image, save_data_to_sql_and_run_model
import numpy as np



def main():
    
    # Création de la table.
    create_table(table_name="picture_predict", name_bdd="neuronal_convolutif")
    
    # Accueil (titre & header).
    st.title("Visualisation réseau neuronal convolutif")
    st.header("Accueil")  
    
    # message pour l'utilisteur
    st.write('Veuillez choisir une image...')
    
    
    # Affichage de l'image
    print_image(index=1)
    
    # enregistrement de l'image dans la table en BDD. & prédiction.
    pred = save_data_to_sql_and_run_model(n_image=1, index=1)
    st.write(pred)
    


    # Affichage du titre de prédictions.
    st.header("Prédictions...")

main()


# essayer de faire un While true et de faire sortir avec une condition.