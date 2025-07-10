from flask import Flask, render_template, request, jsonify
from PIL import Image
import torch
import torchvision.transforms as transforms
import os
from utils import load_model, predict_gesture

# 🔽 ADD THIS block BEFORE loading the model
import gdown

model_path = 'gesture_model.pth'
if not os.path.exists(model_path):
    print("⏬ Downloading model from Google Drive...")
    gdown.download('https://drive.google.com/uc?id=1DyML-h_g_3lO2sO5lusXbQ-ovZrjpPFM', model_path, quiet=False)
else:
    print("✅ Model already exists. Skipping download.")

# 🔽 THEN load the model
model = load_model(model_path)

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
