from flask import Flask, render_template, request, jsonify
from PIL import Image
import moondream as md
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Moondream API
model = md.vl(api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI4NjA5MjgyYy01ZTBlLTQ4ZmUtODMxMi1hMjA4YjEwYjYyODUiLCJpYXQiOjE3MzQ5MzczMjV9.PVx7DfVPp8MshiLLKBJ4CfkuAAdDwu_Qb4Iy3f3-2K4")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    if 'image' not in request.files or not request.form.get('question'):
        return jsonify({"error": "Missing image or question"}), 400

    image = request.files['image']
    question = request.form.get('question')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    img = Image.open(image_path)
    encoded_image = model.encode_image(img)
    answer = model.query(encoded_image, question)["answer"]

    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)