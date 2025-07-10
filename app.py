from flask import Flask, render_template, request, jsonify
import os
from utils import load_model, predict_image
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

model, transform, class_names = load_model('gesture_model.pth')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    image = Image.open(path).convert("RGB")
    prediction = predict_image(model, image, transform, class_names)

    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)

