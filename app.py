from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')  # Pastikan backend non-GUI digunakan
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Koneksi MongoDB (ubah sesuai konfigurasi)
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client['image_processing_db']
collection = db['images']

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def generate_filename(extension):
    return str(uuid.uuid4()) + extension

# Fungsi penyimpanan gambar ke MongoDB
def save_to_db(filename, method, original_path, processed_path, histogram_path):
    data = {
        "filename": filename,
        "method": method,
        "original_path": original_path,
        "processed_path": processed_path,
        "histogram_path": histogram_path
    }
    collection.insert_one(data)
    return str(data['_id'])

def get_all_images():
    return list(collection.find({}, {"_id": 0}))  # Ambil semua data tanpa _id

def delete_image(filename):
    image_data = collection.find_one({"filename": filename})
    if image_data:
        # Hapus file dari storage
        os.remove(image_data["original_path"])
        os.remove(image_data["processed_path"])
        os.remove(image_data["histogram_path"])
        # Hapus dari database
        collection.delete_one({"filename": filename})
        return True
    return False

# Fungsi Histogram
def plot_histogram(image, filename):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    plt.figure()
    plt.hist(gray.ravel(), bins=256, range=[0, 256], density=True, color='gray', alpha=0.75)
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    hist_filename = os.path.join(app.config['UPLOAD_FOLDER'], generate_filename('.png'))
    plt.savefig(hist_filename)
    plt.close()
    return hist_filename

# Fungsi Pemrosesan Citra
def apply_processing(image, method, filename):
    if method == 'HE':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        processed = cv2.equalizeHist(gray)
    elif method == 'AHE':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        processed = clahe.apply(gray)
    elif method == 'CLAHE':
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_eq = clahe.apply(l)
        processed = cv2.merge((l_eq, a, b))
        processed = cv2.cvtColor(processed, cv2.COLOR_LAB2BGR)
    else:
        return None, None

    processed_filename = generate_filename('.png')
    processed_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
    cv2.imwrite(processed_path, processed)

    hist_filename = plot_histogram(processed, processed_filename)
    return processed_path, hist_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    method = request.form['method']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    extension = os.path.splitext(file.filename)[1]
    filename = generate_filename(extension)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    image = cv2.imread(filepath)
    if image is None:
        return jsonify({'error': 'Failed to read image'})

    processed_path, hist_filename = apply_processing(image, method, filename)
    if not processed_path:
        return jsonify({'error': 'Invalid method'})

    # Simpan ke database
    save_to_db(filename, method, filepath, processed_path, hist_filename)

    return jsonify({'original': filepath, 'processed': processed_path, 'histogram': hist_filename})

@app.route('/images', methods=['GET'])
def get_images():
    return jsonify(get_all_images())

@app.route('/delete', methods=['POST'])
def delete():
    filename = request.json.get('filename')
    if delete_image(filename):
        return jsonify({'message': 'Deleted successfully'})
    return jsonify({'error': 'File not found'})

if __name__ == '__main__':
    app.run(debug=True)
