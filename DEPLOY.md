# Dokumentasi Proses Membuat Artifact Registry dan Deploy ke Cloud Run

Dokumentasi ini menjelaskan langkah-langkah mulai dari pembuatan Artifact Registry, pembangunan Docker image, hingga mendeploy aplikasi ke Google Cloud Run.

## Persiapan Awal
Sebelum memulai, pastikan Anda sudah melakukan hal-hal berikut:

* Memiliki Google Cloud Platform (GCP) account.
* Telah mengaktifkan Billing untuk project di GCP.
* Telah mengaktifkan Cloud Run dan Artifact Registry API.

### 1. Install Google Cloud SDK (gcloud CLI)
Jika Anda belum menginstall gcloud CLI, silakan mengikuti petunjuk instalasi di [Google Cloud SDK installation guide](https://cloud.google.com/sdk/docs/install).

Setelah itu, pastikan Anda dapat menjalankan perintah gcloud di terminal dengan memverifikasi versi yang terinstal:

```bash
gcloud --version
```
### 2. Login ke Google Cloud
Login menggunakan akun Google Cloud Anda:
```bash
gcloud auth login
```
Pilih project yang sesuai:
```bash
gcloud config set project YOUR_PROJECT_ID
```

## Langkah 1: Membuat Artifact Registry
Artifact Registry digunakan untuk menyimpan dan mengelola Docker images yang akan dideploy ke Cloud Run.

### 1.1. Membuat Repositori di Artifact Registry
Untuk membuat repositori baru di Artifact Registry, gunakan perintah berikut:
```bash
gcloud artifacts repositories create REPOSITORY_NAME \
  --repository-format=docker \
  --location=asia-southeast2
```

* `REPOSITORY_NAME`: Nama repositori yang ingin Anda buat.
* `--location=asia-southeast2`: Lokasi repositori di Jakarta.

Verifikasi repositori sudah dibuat dengan perintah:
```bash
gcloud artifacts repositories list --location=asia-southeast2
```

### 1.2. Autentikasi Docker ke Artifact Registry
Agar Docker dapat mengakses Artifact Registry, lakukan konfigurasi autentikasi dengan perintah berikut:
```bash
gcloud auth configure-docker asia-southeast2-docker.pkg.dev
```

## Langkah 2: Membangun Docker Image
Untuk mendeploy aplikasi ke Cloud Run, kita perlu membangun Docker image dari aplikasi Anda.

### 2.1. Menyusun Dockerfile
Di dalam direktori proyek Anda, buat file Dockerfile dengan konten sebagai berikut (misalnya untuk aplikasi Node.js dengan Express):
```bash
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
EXPOSE 5000

# Perintah untuk menjalankan aplikasi Flask
CMD ["python", "app.py"]
```

### 2.2. Membangun Docker Image
Bangun Docker image menggunakan perintah `docker build` dengan menandai image yang ingin Anda buat.
```bash
docker build -t my-express-app .
```
Gantilah `my-express-app` dengan nama image yang sesuai.

### 2.3. Menandai Docker Image untuk Artifact Registry
Setelah image berhasil dibangun, Anda perlu menandainya dengan nama yang sesuai dengan repositori di Artifact Registry. Formatnya adalah:
```bash
[LOCATION]-docker.pkg.dev/[PROJECT_ID]/[REPOSITORY_NAME]/[IMAGE_NAME]:[TAG]
```
Misalnya:
```bash
docker tag my-express-app asia-southeast2-docker.pkg.dev/YOUR_PROJECT_ID/my-repository/my-express-app:latest
```
Gantilah:

* `YOUR_PROJECT_ID` dengan ID project GCP Anda.
* `my-repository` dengan nama repositori yang telah Anda buat di Artifact Registry.

### 2.4. Push Docker Image ke Artifact Registry
Sekarang, upload image yang telah Anda bangun ke Artifact Registry menggunakan perintah `docker push`:
```bash
docker push asia-southeast2-docker.pkg.dev/YOUR_PROJECT_ID/my-repository/my-express-app:latest
```
Verifikasi apakah image telah berhasil di-push ke Artifact Registry:
```bash
gcloud artifacts docker images list asia-southeast2-docker.pkg.dev/YOUR_PROJECT_ID/my-repository
```

## Langkah 3: Mendeploy Aplikasi ke Cloud Run
Setelah image berhasil di-push ke Artifact Registry, langkah selanjutnya adalah mendeploy aplikasi ke Cloud Run.

### 3.1. Deploy ke Cloud Run
Gunakan perintah berikut untuk mendeploy Docker image ke Cloud Run:
```bash
gcloud run deploy my-express-app \
  --image asia-southeast2-docker.pkg.dev/YOUR_PROJECT_ID/my-repository/my-express-app:latest \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated
```
Penjelasan parameter:

* `my-express-app`: Nama aplikasi yang akan ditampilkan di Cloud Run.
* `--image`: Alamat Docker image yang ada di Artifact Registry.
* `--platform managed`: Menunjukkan bahwa Anda menggunakan platform Cloud Run yang dikelola.
* `--region asia-southeast2`: Lokasi tempat aplikasi akan di-deploy (di Jakarta).
* `--allow-unauthenticated`: Memberikan akses publik ke aplikasi yang di-deploy (opsional).

### 3.2. Verifikasi Deploy
Setelah proses deploy selesai, periksa URL aplikasi yang di-deploy yang akan ditampilkan di terminal setelah berhasil deploy. Anda dapat mengakses aplikasi melalui URL tersebut.

## Langkah 4: Memverifikasi dan Mengelola Cloud Run

### 4.1. Melihat Status Cloud Run
Untuk melihat daftar layanan yang di-deploy di Cloud Run, gunakan perintah berikut:
```bash
gcloud run services list --platform managed --region asia-southeast2
```

### 4.2. Melihat URL Aplikasi
Setelah berhasil deploy, Anda dapat mendapatkan URL aplikasi yang di-deploy dengan perintah:
```bash
gcloud run services describe my-express-app --platform managed --region asia-southeast2
```
URL aplikasi akan ditampilkan di bagian `URL` pada output perintah di atas.

