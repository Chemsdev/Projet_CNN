import streamlit as st
from streamlit_drawable_canvas import st_canvas
from tensorflow import keras
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
import matplotlib.pyplot as plt
import plotly.express as px




st.title("Visualisation des couches ")


model = load_model('my_model2.h5')
st.title("Draw your number here")



canvas_result = st_canvas(
    height=300,width=400,
    fill_color='#ffffff', background_color='#000000',
    stroke_width=10,
    stroke_color='#ffffff',
    drawing_mode='freedraw',
    key='canvas')

if canvas_result.image_data is not None :
  img = cv2.resize(canvas_result.image_data.astype('uint8'),(28,28))
  
  

if st.button('predict') :
  test_x = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  pred = model.predict((test_x.reshape(-1,28,28,1))/255)
  st.write(f'result: {np.argmax(pred[0])}')
  
  # visualisation des layers, attention a l'indentation
  successive_outputs = [layer.output for layer in model.layers[0:]]
  visualization_model = tf.keras.models.Model(inputs = model.input, outputs = successive_outputs)
  test = ((test_x).reshape((-1,28,28,1)))/255.0
  successive_feature_maps = visualization_model.predict(test)
  layer_names = [layer.name for layer in model.layers]
  for layer_name, feature_map in zip(layer_names, successive_feature_maps):
       if len(feature_map.shape) == 4:
              n_features = feature_map.shape[-1] 
              size = feature_map.shape[ 1]  
              display_grid = np.zeros((size, size * n_features))
              for i in range(n_features):
                     x  = feature_map[-1, :, :, i]
                     x -= x.mean()
                     x /= x.std ()
                     x *=  64
                     x += 128
                     x  = np.clip(x, 0, 255).astype('uint8')
                     display_grid[:, i * size : (i + 1) * size] = x
                     scale = 20. / n_features
              fig = plt.figure( figsize=(scale * n_features, scale) )
              plt.title ( layer_name )
              plt.grid  ( False )
              plt.imshow( display_grid, aspect='auto', cmap='viridis' )
              st.pyplot(fig)
  
 
 



