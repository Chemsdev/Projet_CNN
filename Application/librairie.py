
# Import des librairies.
from sqlalchemy import create_engine
from sqlalchemy import inspect
import streamlit as st
import numpy as np
import pymysql
import pandas as pd

# Import de la data
x_train = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet/data/train.csv")
x_test  = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet\data/test.csv")

# connexion à la base de données.
conn=pymysql.connect(host='localhost',port=int(3306),user='root', passwd='', db='neuronal_convolutif')

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
    

    
# Fonction : permettent d'envoyer l'image choisis en BDD.
# La fonction prend en paramètre : l'index de l'image, le test_set, et la connexion à la BDD.
def send_sql_table(index:int, test=x_test, conn=conn):
    test  = np.array(test)
    features = test[index]
    cursor = conn.cursor()
    
    # Placement des colonnes de la table pour la requete
    columns_table=[]
    for i in range(len(features)):
        columns_table.append(f"pixel{i}")
    columns_table.insert(0, "label")
    
    # Placement des valeurs de la table pour la requete
    values_table=[]
    for i in features:
        values_table.append(str(i))
    values_table.insert(0, '8')
    
    # On envoie les données de l'image choisis dans la table de notre bdd
    sql = f"INSERT INTO picture_predict ({', '.join(columns_table)}) VALUES ({', '.join(['%s' for i in range(785)])})"
    cursor.execute(sql, values_table)
    conn.commit()
    conn.close()
    
# Fonction : permettent d'afficher une image sur notre site web.
# La fonction prend en paramètre : l'index de l'image, le test set, et la clé identificateur du bouton.
def print_image(index:int, test=x_test, n_image=int):
    
    # Création de l'image
    test = np.array(test)
    img  = test[index]
    img  = img.reshape((28, 28))
    
    # Affichage de l'image avec le boutton
    st.image(img, width=80)
    if st.button('choisir', key=f'image_{n_image}'):
        st.write(f"Vous avez choisi image d'index {n_image}.")
        send_sql_table(index=index, test=x_test, conn=conn)

