
# Import des librairies.
from sqlalchemy import create_engine
from sqlalchemy import inspect
import streamlit as st
import numpy as np
import pymysql
import pandas as pd

# Fonction permettent de créer une table.
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

