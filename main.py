import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from predict import predict_dinosaur, model
from train import get_train_generator

app = Flask(__name__)
CORS(app)


@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    img_path = './temp_image.jpg'
    image_file.save(img_path)

    predicted_label = predict_dinosaur(img_path, model, get_train_generator().class_indices)

    os.remove(img_path)

    return jsonify({'predicted_label': predicted_label})



if __name__ == '__main__':
    app.run(port=5000)