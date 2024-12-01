import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Menonaktifkan penggunaan GPU
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

# Inisialisasi Flask app
app = Flask(__name__)
# Load model TensorFlow (.h5)
model = tf.keras.models.load_model('model.h5', compile=False)

# Route untuk endpoint prediksi
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Mengambil data input JSON dari request
        data = request.get_json()

        # Validasi jumlah input
        if 'input' not in data or len(data['input']) != 50:
            return jsonify({'error': 'Input must be a list of 50 numerical values.'}), 400
        
        # Asumsikan data input adalah array angka, sesuai dengan format input model Anda
        input_data = np.array(data['input']).reshape(1, -1)  # Sesuaikan shape dengan kebutuhan model Anda
        
        # Dimensi Big Five Personality
        traits = ['Keterbukaan Sosial, Energi, dan Antusiasme', 'Kestabilan Emosi', 'Kesepakatan', 'Ketelitian', 'Keterbukaan terhadap Pengalaman']

        # Lakukan prediksi
        predictions = model.predict(input_data)

        output = {traits[i]: float(predictions[i]) for i in range(5)}
        return jsonify({'prediction': output})
    except Exception as e:
        return jsonify({'error': str(e)})

# Jalankan aplikasi Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

