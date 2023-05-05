
# Import des librairies.
import streamlit as st
import numpy as np
import pymysql
import pandas as pd
import random

# Import des utilitaires pour le modèle.
import tensorflow as tf
from tensorflow import keras

# =========================== Utilitaires =======================================>

# Import de la data.
x_train = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet/data/train.csv")
x_test  = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet\data/test.csv")

# connexion à la base de données.
conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')

# importation du modèle 
model = tf.keras.models.load_model("C:/Users/Chems Ounissi/Desktop/CNN_projet/my_model2.h5")

# =========================== Les fonctions ====================================>

# Fonction permettent de créer 2 tables.
def create_tables_2_tables(name_bdd: str):
    
    # Connexion à la base de données
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db=name_bdd)
    cursor = conn.cursor()

    # Création de la table "images" avec 784 colonnes pour les features
    col_names = ['feature_' + str(i) for i in range(784)]
    col_names_str = ','.join([f'{name} REAL' for name in col_names])
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS images
                (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, {col_names_str})''')
    print("Table 'images' créée avec succès.")

    # Création de la table "predictions" avec les colonnes "y_true" et "y_pred"
    cursor.execute('''CREATE TABLE IF NOT EXISTS predictions
                (id int NOT NULL DEFAULT 0,
                y_true TEXT,
                index_image TEXT,
                y_pred TEXT,
                image_id INTEGER,
                FOREIGN KEY (image_id) REFERENCES images(id))''')
    print("Table 'predictions' créée avec succès.")

    # Fermeture de la connexion à la base de données
    conn.commit()
    conn.close()

# =============================================================================>

# Fonction permettent d'éxécuter le modèle et d'enregistrer les données dans 2 tables.
def send_sql_table_2_tables(prediction, index:int, features, y_true):
    
    # connexion à la bdd.
    conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')
    cursor = conn.cursor()
    
    # On génère code id unique.
    code_id = "".join([str(random.randint(0, 10)) for _ in range(5)])  
    
    #=============================== MISE EN PLACE TABLE IMAGES =====================================>
    
    # Mise en place des noms de colonnes de la Table.
    columns_table=[f"feature_{i}"for i in range(len(features))]
    columns_table.insert(0, "id")
    
    # Mise en places des données à insérer dans la table.
    values_table=[str(i) for i in features]
    values_table.insert(0, str(code_id))
    
    # Insertion des features dans la table images.
    sql = f"INSERT INTO images ({', '.join(columns_table)}) VALUES ({', '.join(['%s' for i in range(785)])})"
    cursor.execute(sql, values_table)
    
    # =============================== MISE EN PLACE TABLE PREDICTIONS ===============================>
    
    # Préparation des données à l'envoie.
    columns_table =  ["id", "index_image", "y_true", "y_pred", "image_id"]
    
    if int(y_true) == int(prediction.item()):
        values_table  =  [code_id,  index,  "oui",   str(prediction.item()),  code_id]
    else:
        values_table  =  [code_id,  index,  "non",   str(prediction.item()),  code_id]  
        
    # Insertion des résultats dans la table predictions.
    sql = f"INSERT INTO predictions ({', '.join(columns_table)}) VALUES ({', '.join(['%s' for i in range(5)])})"
    cursor.execute(sql, values_table)
    
    # Fermeture de la connexion.
    conn.commit()
    conn.close()
    
    # On retourne la prédiction.
    return prediction

# =============================================================================>

# Fonction permettent de supprimer 2 tables.
def delete_content_tables():
    conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    cursor.execute("DELETE FROM images")
    cursor.execute("DELETE FROM canvas")
    conn.commit()
    cursor.close()
    conn.close()
    
# =============================================================================>


