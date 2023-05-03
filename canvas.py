
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from tensorflow import keras
import cv2
import numpy as np
from tensorflow.keras.models import load_model




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
  
 