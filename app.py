from flask import Flask, render_template, request, jsonify
from PIL import Image
import torch
import torchvision.transforms as transforms
import os
from utils import load_model, predict_gesture

app = Flask(__name__)
model = load_model('gesture_model.pth')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file:
        filepath = os.path.join('static', 'uploaded.png')
        file.save(filepath)
        prediction = predict_gesture(filepath, model)
        return jsonify({'gesture': prediction})
    return jsonify({'error': 'No file received'}), 400

if __name__ == '__main__':
    app.run(debug=True)

