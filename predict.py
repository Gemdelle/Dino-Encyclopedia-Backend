from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

from train import get_train_generator

# Cargar modelo entrenado en lugar de crearlo desde cero
model = load_model('dino_classifier_model.h5')

# Mismo código de predicción
def predict_dinosaur(img_path, model, class_indices):
    img = load_img(img_path, target_size=(224, 224))  # Ajustar tamaño
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalización correcta

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)

    class_labels = list(class_indices.keys())
    return class_labels[predicted_class]

# Prueba de predicción con una imagen
img_path = './image_to_validate/trex.png'
predicted_label = predict_dinosaur(img_path, model, get_train_generator().class_indices)
print(f"Predicted Dinosaur: {predicted_label}")
