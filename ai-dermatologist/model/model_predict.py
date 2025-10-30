import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

model = tf.keras.models.load_model('skin_disease_model.h5')

def predict_image(img_path, labels):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_array)
    index = np.argmax(prediction)
    print(f"Predicted Disease: {labels[index]} ({prediction[0][index]*100:.2f}%)")
