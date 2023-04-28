
# Import des librairies.
from sqlalchemy import create_engine
from sqlalchemy import inspect
import streamlit as st
import numpy as np
import pymysql
import pandas as pd
import pickle

# Import des utilitaires pour le modèle.
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Importation du modèle.
with open("C:/Users/Chems Ounissi/Desktop/CNN_projet/baseline.pkl", 'rb') as f:
    model = pickle.load(f)

# Import de la data.
x_train = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet/data/train.csv")
x_test  = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet\data/test.csv")

# connexion à la base de données.
conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')

# Fonction permettent de créer une table.
# La fonction prend en paramètre le nom de la table et le nom de la base de données.
def create_table(table_name:str, name_bdd:str):  
    
    # connexion à la base de données.
    engine=create_engine(f'mysql+pymysql://root:@localhost/{name_bdd}')
    inspector=inspect(engine)
    
    # Si la table n'existe pas on la créer.
    if not table_name in inspector.get_table_names():
        
        # Initialisation des 784 colonnes (pixels).
        df = pd.DataFrame({f'pixel{i}':[] for i in range(0,784)})
        
        # Typage des colonnes de la Table SQL.
        for i in df:
            df[i]=df[i].astype('int64')
            
        # Insérer la Target en première position.
        label = ''
        df.insert(loc=0, column='label', value=label)
        
        # envoie du DataFrame sur SQL.
        df.to_sql(name=table_name, con=engine, if_exists='fail', index=False)
          
    # Message pour l'utilisateur. 
    print(f"Création de la table {table_name} avec succès.")
    
# Fonction : permettent de faire la prédiction.
# La fonction prend en paramètre : l'index de l'image, le test set, et la clé identificateur du bouton.
def make_prediction(data, model=model):
    prediction = model.predict(data/255)
    return prediction
    
# Fonction : permettent d'envoyer l'image choisis en BDD.
# La fonction prend en paramètre : l'index de l'image, le test_set, et la connexion à la BDD.
def send_sql_table(index:int, test=x_test):
    
    # connexion à la BDD.
    conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')
    
    # On saisit l'image d'index dans le test set.
    test  = np.array(test)
    features = test[index]
    cursor = conn.cursor()

    # On fait la prédiction.
    pred = make_prediction(features, model=model)
    
    # Placement des colonnes de la table pour la requete.
    columns_table=[]
    for i in range(len(features)):
        columns_table.append(f"pixel{i}")
    columns_table.insert(0, "label")
    
    # Placement des valeurs de la table pour la requete.
    values_table=[]
    for i in features:
        values_table.append(str(i))
    values_table.insert(0, pred)
    
    # On envoie les données de l'image choisis dans la table de notre bdd.
    sql = f"INSERT INTO picture_predict ({', '.join(columns_table)}) VALUES ({', '.join(['%s' for i in range(785)])})"
    cursor.execute(sql, values_table)
    conn.commit()
    conn.close()
    
    # On retourne la prédiction.
    return pred
    
# Fonction : permettent d'afficher une image sur notre site web.
# La fonction prend en paramètre : l'index de l'image, le test set, et la clé identificateur du bouton.
def print_image(index:int, test=x_test, n_image=int):
    
    # Création de l'image
    test = np.array(test)
    img  = test[index]
    img  = img.reshape((28, 28))
    
    # Affichage de l'image 
    st.image(img, width=80)
    

# Si l'utilisateur clique sur le bouton, on envoie la data dans la table en BDD  et on run le modèle.
def save_data_to_sql_and_run_model(n_image, index):
    if st.button('choisir', key=f'image_{n_image}'):
        pred = send_sql_table(index=index, test=x_test)
    return pred


