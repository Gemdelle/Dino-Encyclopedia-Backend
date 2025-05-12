import tensorflow as tf
import numpy as np
from app.ml.train import get_data_generators
import os
from typing import Optional

# Define base path for data
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
_model: Optional[tf.keras.Model] = None

def load_model() -> Optional[tf.keras.Model]:
    """
    Loads the model if it exists, returns None if the model file is not found.
    """
    model_path = os.path.join(DATA_DIR, 'models', 'dino_analyzer_model.keras')
    if not os.path.exists(model_path):
        return None
    return tf.keras.models.load_model(model_path)

def get_model() -> Optional[tf.keras.Model]:
    """
    Returns the loaded model or attempts to load it if not already loaded.
    """
    global _model
    if _model is None:
        _model = load_model()
    return _model

def predict_dinosaur(image_path: str, class_indices: dict) -> dict:
    """
    Predicts dinosaur class from image. Returns error information if model is not available.
    """
    model = get_model()
    if model is None:
        return {
            "error": "Model not available",
            "message": "The dinosaur classification model has not been trained yet. Please train the model first."
        }
    
    if not os.path.exists(image_path):
        return {
            "error": "File not found",
            "message": f"The image file {image_path} was not found."
        }

    try:
        img = tf.keras.preprocessing.image.load_img(
            image_path, target_size=(224, 224)
        )
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, 0)
        
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        
        # Invert the class dictionary
        class_mapping = {v: k for k, v in class_indices.items()}
        predicted_name = class_mapping[predicted_class]
        
        return {
            "success": True,
            "prediction": predicted_name,
            "confidence": float(predictions[0][predicted_class])
        }
    except Exception as e:
        return {
            "error": "Prediction failed",
            "message": str(e)
        }

# Initialize model (but don't fail if not available)
_model = load_model() 