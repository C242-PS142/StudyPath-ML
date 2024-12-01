# Gunakan image dasar Python
FROM python:3.12.7

# Tentukan direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt dan install dependensi
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi ke dalam container
COPY . .

# Tentukan port yang akan digunakan oleh container
EXPOSE 8080

# Perintah untuk menjalankan aplikasi Flask
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
