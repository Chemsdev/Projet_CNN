
# Import des librairies.
from sqlalchemy import create_engine
from sqlalchemy import inspect
import streamlit as st
import numpy as np
import pymysql
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


with open("C:/Users/Chems Ounissi/Desktop/CNN_projet/baseline.pkl", 'rb') as f:
    model = pickle.load(f)

x_train = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet/data/train.csv")
x_test  = pd.read_csv("C:/Users/Chems Ounissi/Desktop/CNN_projet\data/test.csv")

conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')

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
    
def make_prediction(data, model=model):
    prediction = model.predict(data/255)
    return prediction
    
def send_sql_table(index:int, test=x_test):
    conn=pymysql.connect(host='localhost', port=int(3306), user='root', passwd='', db='neuronal_convolutif')
    test  = np.array(test)
    features = test[index]
    cursor = conn.cursor()
    pred = make_prediction(features, model=model)
    columns_table=[]
    for i in range(len(features)):
        columns_table.append(f"pixel{i}")
    columns_table.insert(0, "label")
    values_table=[]
    for i in features:
        values_table.append(str(i))
    values_table.insert(0, pred)
    sql = f"INSERT INTO picture_predict ({', '.join(columns_table)}) VALUES ({', '.join(['%s' for i in range(785)])})"
    cursor.execute(sql, values_table)
    conn.commit()
    conn.close()
    return pred

def print_image(index:int, test=x_test, n_image=int):
    test = np.array(test)
    img  = test[index]
    img  = img.reshape((28, 28))
    st.image(img, width=80)
    
def save_data_to_sql_and_run_model(n_image, index):
    if st.button('choisir', key=f'image_{n_image}'):
        pred = send_sql_table(index=index, test=x_test)
    return pred


