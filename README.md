# Histogram Enhancement App

## 📌 Overview
Histogram Enhancement App adalah aplikasi berbasis web yang digunakan untuk meningkatkan kualitas gambar menggunakan tiga metode utama dalam pemrosesan citra: **Histogram Equalization (HE), Adaptive Histogram Equalization (AHE), dan Contrast Limited Adaptive Histogram Equalization (CLAHE)**. Aplikasi ini dikembangkan menggunakan **Python, OpenCV, Flask, dan MongoDB** untuk menyimpan metadata hasil pemrosesan.

## 🛠️ Features
- **Upload gambar** dan pilih metode pemrosesan (HE, AHE, atau CLAHE).
- **Tampilkan hasil sebelum & sesudah pemrosesan** dalam bentuk gambar.
- **Tampilkan histogram intensitas piksel** untuk analisis distribusi piksel.
- **Simpan hasil pemrosesan dalam database MongoDB**.
- **Hapus gambar yang telah diproses** dari database dan sistem.

## 📂 Folder Structure
```
Histogram_Enhancement_App/
│── static/             # Folder untuk menyimpan gambar hasil pemrosesan
│── templates/          # Folder untuk file HTML (frontend)
│── app.py              # Main backend file menggunakan Flask
│── README.md           # Dokumentasi proyek
│── requirements.txt     # Dependencies untuk menjalankan aplikasi
```

## 🚀 Installation & Setup
### 1️⃣ Install Dependencies
Pastikan kamu memiliki **Python** dan **pip** terinstall di sistemmu, lalu jalankan perintah berikut:
```bash
pip install -r requirements.txt
```

### 2️⃣ Jalankan MongoDB
Pastikan MongoDB sudah berjalan secara lokal atau gunakan layanan cloud seperti MongoDB Atlas.

### 3️⃣ Jalankan Flask App
Jalankan aplikasi dengan perintah berikut:
```bash
python app.py
```
Akses aplikasi melalui browser di: `http://127.0.0.1:5000/`

## 🖼️ How to Use
1. **Upload gambar** melalui antarmuka web.
2. **Pilih metode pemrosesan** (HE, AHE, atau CLAHE).
3. **Lihat hasil pemrosesan** dan histogramnya.
4. **Hapus gambar** jika tidak diperlukan lagi.

## 📌 Technologies Used
- **Python** (Backend Processing)
- **Flask** (Web Framework)
- **OpenCV** (Image Processing)
- **Matplotlib** (Histogram Visualization)
- **MongoDB** (Database for storing metadata)

## 📜 License
This project is licensed under the **MIT License**.

## 🤝 Contributing
Jika ingin berkontribusi, silakan lakukan **fork** repository ini dan ajukan **pull request** dengan perubahan yang diusulkan.

## 📞 Contact
Jika ada pertanyaan atau kendala dalam menggunakan aplikasi ini, silakan hubungi saya melalui email: **mozessapari@gmail.com**.

