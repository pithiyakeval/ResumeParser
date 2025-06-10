from flask import Flask, jsonify, request
import os
from parser import parse_resume
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

@app.route('/')
def index():
    return "Backend is Running Successfully"

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('resume')
    if not file:
        return jsonify({"error": "No file part"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    print("✅ Resume saved at:", filepath)  

    data = parse_resume(filepath)
    print("✅ Parsing done")

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
