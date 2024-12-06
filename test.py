import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Menonaktifkan penggunaan GPU
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import joblib

# Inisialisasi Flask app
app = Flask(__name__)
# Load model TensorFlow (.h5)
model = tf.keras.models.load_model('model3.h5', compile=False)

scaler_X = joblib.load('scaler_X.pkl')  # Muat scaler untuk fitur input
scaler_y = joblib.load('scaler_y.pkl')  # Muat scaler untuk target output

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

        # Pastikan semua elemen adalah angka
        try:
            input_data = np.array(data['input'], dtype=float).reshape(1, -1)
        except ValueError:
            return jsonify({'error': 'All elements in the input list must be numerical values.'}), 400

        # Terapkan MinMaxScaler pada input data yang masuk
        input_data_scaled = scaler_X.transform(input_data)

        predictions = model.predict(input_data_scaled).flatten()

        # Inverse transformasi prediksi untuk mengembalikannya ke skala asli
        predictions_original = scaler_y.inverse_transform(predictions.reshape(1, -1)).flatten()

        # Format hasil prediksi
        # output = predictions_original.tolist()
        # output = {traits[i]: float(predictions[i]) for i in range(len(traits))}
        output = {traits[i]: format(float(predictions_original[i]), '.15f').rstrip('0').rstrip('.') for i in range(len(traits))}

        return jsonify({'predictions': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Jalankan aplikasi Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

