
# Import des librairies.
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import create_engine, MetaData, Table
import streamlit as st
import numpy as np
import pymysql
import pandas as pd
import pickle
import random

# Import des utilitaires pour le modèle.
import tensorflow as tf
from tensorflow import keras

# =========================== Utilitaires ====================================>

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
                y_pred TEXT,
                image_id INTEGER,
                FOREIGN KEY (image_id) REFERENCES images(id))''')
    print("Table 'predictions' créée avec succès.")

    # Fermeture de la connexion à la base de données
    conn.commit()
    conn.close()

# =============================================================================>

# Fonction permettent d'enregistrer les données dans 2 tables.
def send_sql_table_2_tables(index:int, test=x_test, model=model):

    # connexion à la bdd
    conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')
    
    # sélection de l'image
    test  = np.array(test)
    features = test[index]
    cursor = conn.cursor()
    
    # on réalise la prédiction
    prediction = model.predict(((features).reshape((-1,28,28,1)))/255.0)
    prediction = np.argmax(prediction, axis=1)
    
    # Vérifier si l'ID existe déjà dans la table 'images'
    cursor.execute("SELECT id FROM images WHERE id=%s", (index,))
    result = cursor.fetchone()
    
    # Si l'id n'est pas présent, on envoie les données dans la BDD.
    if result is None:
        
        # Mise en place des colonnes et valeur à insérer.
        columns_table=[]
        for i in range(len(features)):
            columns_table.append(f"feature_{i}")
        columns_table.insert(0, "id")
        
        values_table=[]
        for i in features:
            values_table.append(str(i))
        values_table.insert(0, str(index))
        
        # Insertion des features dans la table images
        sql = f"INSERT INTO images ({', '.join(columns_table)}) VALUES ({', '.join(['%s' for i in range(785)])})"
        cursor.execute(sql, values_table)
        
        # Insertion des résultats dans la table predictions.
        v=random.randint(0,10)
        columns_table = ["y_true", "y_pred", "image_id"]
        values_table = [v, str(prediction.item()), str(index)]
        sql = f"INSERT INTO predictions ({', '.join(columns_table)}) VALUES ({', '.join(['%s' for i in range(3)])})"
        cursor.execute(sql, values_table)
        
        conn.commit()
        conn.close()
    else:
        pass
    return prediction


# =============================================================================>

# Fonction permettent de supprimer 2 tables.
def delete_content_tables():
    conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    cursor.execute("DELETE FROM images")
    conn.commit()
    cursor.close()
    conn.close()

# =============================================================================>