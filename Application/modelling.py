# Import des librairies
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# Import de la data
x_train = pd.read_csv("train.csv")
x_test  = pd.read_csv("test.csv")

# Convertion en numpy array
x_train = np.array(x_train) 
x_test  = np.array(x_test) 

