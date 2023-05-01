
# Import des librairies.
from sqlalchemy import create_engine
from sqlalchemy import inspect
import streamlit as st
import numpy as np
import pymysql
import pandas as pd

# Import des utilitaires pour le modèle.
import tensorflow as tf
from tensorflow import keras
from bdd_2_tables import send_sql_table_2_tables

# =========================== Utilitaires ====================================>

# Import de la data.
x_train = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet/data/train.csv")
x_test  = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet\data/test.csv")

# connexion à la base de données.
conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')

# importation du modèle 
model = tf.keras.models.load_model("C:/Users/Chems Ounissi/Desktop/CNN_projet/my_model2.h5")

# =========================== Les fonctions ====================================>

# Fonction permettent de créer une table.
def create_table(table_name:str, name_bdd:str):  
    engine=create_engine(f'mysql+pymysql://root:@localhost/{name_bdd}')
    inspector=inspect(engine)
    if not table_name in inspector.get_table_names():
        df = pd.DataFrame({f'pixel{i}':[] for i in range(0,784)})
        for i in df:
            df[i]=df[i].astype('int64')
        label = ''
        df.insert(loc=0, column='label', value=label)
        df.to_sql(name=table_name, con=engine, if_exists='fail', index=False)
    print(f"Création de la table {table_name} avec succès.")

# =============================================================================>
   
# Fonction : permettent d'afficher une image sur notre site web.
def print_image(index:int, test=x_test):
    style = """
    img {
        border-radius: 5px;
        transition: transform 0s ease-in-out;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5);
    }
    
    img:hover {
        transform: scale(1.1);
    }
    """
    test = np.array(test)
    img  = test[index]
    img  = img.reshape((28, 28))
    st.write(f'<style>{style}</style>', unsafe_allow_html=True)
    st.image(img, width=80)

# =============================================================================>
   
# Fonction : permettent d'envoyer l'image choisis en BDD et d'éxécuter le modèle.
def send_sql_table(index:int, test=x_test, model=model):

    conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')
    test  = np.array(test)
    features = test[index]
    cursor = conn.cursor()
    
    prediction = model.predict(((features).reshape((-1,28,28,1)))/255.0)
    prediction = np.argmax(prediction, axis=1)
    
    columns_table=[]
    for i in range(len(features)):
        columns_table.append(f"pixel{i}")
    columns_table.insert(0, "label")
    
    values_table=[]
    for i in features:
        values_table.append(str(i))
    values_table.insert(0, prediction.item())
    
    sql = f"INSERT INTO picture_predict ({', '.join(columns_table)}) VALUES ({', '.join(['%s' for i in range(785)])})"
    cursor.execute(sql, values_table)
    conn.commit()
    conn.close()
    
    return prediction

# =============================================================================>

# Fonction permettent de placer une image de fond pour site web.
def background(url:str):
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url({url});
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
    )

# =============================================================================>

# Fonction permettent de charger des images en local.
def CSS_picture(predict):
    picture = f"image pred/{predict.item()}.jpg"
    st.write(unsafe_allow_html=False)
    st.image(picture, width=300)

# =============================================================================>

# Fonction permettent d'afficher les images
def column_picture():
    
    # Affichage des images.
    col1, col2, col3 = st.columns(3)
    finish=False
    with col1:
        for i in (17, 12, 5):
            print_image(index=i)            
            if st.button("prédire", key=i):
                pred = send_sql_table_2_tables(index=i)
                finish=True
                
    with col2:
        for i in (0, 10, 44):
            print_image(index=i)
            if st.button("prédire", key=i):
                pred = send_sql_table_2_tables(index=i)
                finish=True
    
    with col3:
        for i in (4, 50, 2):
            print_image(index=i)            
            if st.button("prédire", key=i):
                pred = send_sql_table_2_tables(index=i)
                finish=True
    
    # Affichage du résultat.
    if finish:
        st.title("Prédictions...")
        st.subheader(f"Le modèle à trouver !")
        CSS_picture(predict=pred)

# =============================================================================

# Fonction permettent de supprimer le contenu d'une table.
def delete_table(table):
    conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')
    cursor = conn.cursor()
    delete_query = f"DELETE FROM {table};"
    cursor.execute(delete_query)
    conn.commit()
    cursor.close()
    conn.close()
    
# =============================================================================

