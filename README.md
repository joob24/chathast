# Aplikasi Enkripsi Pesan Berbasis Streamlit

Aplikasi ini dibuat menggunakan Streamlit untuk membuat pesan teks yang dienkripsi dengan password yang hanya berlaku selama 10 menit. Selain itu, aplikasi memungkinkan penerima pesan untuk membaca pesan dengan memasukkan hash enkripsi dan password dalam jangka waktu 10 menit.

## Fitur
1. Enkripsi pesan dengan password yang berlaku selama 10 menit.
2. Dekripsi pesan dengan password yang sama dalam waktu 10 menit.

## Instalasi dan Menjalankan Aplikasi

1. Pastikan Python 3.7 atau lebih baru sudah terinstall di komputer Anda.
2. Instal dependency yang diperlukan dengan perintah berikut:
   ```
   pip install streamlit cryptography
   ```
3. Jalankan aplikasi dengan perintah:
   ```
   streamlit run app.py
   ```
4. Akses aplikasi pada browser di alamat yang diberikan oleh Streamlit (biasanya http://localhost:8501).

## Cara Penggunaan

- Buka aplikasi di browser.
- Pilih fitur "Enkripsi Pesan" untuk membuat pesan hash dengan password aktif selama 10 menit.
- Bagikan hash hasil enkripsi dan password kepada penerima.
- Penerima menggunakan fitur "Dekripsi Pesan" dengan memasukkan hash beserta password untuk membaca pesan selama 10 menit setelah pembuatan.

Jika melebihi waktu 10 menit, pesan tidak dapat dibuka lagi meskipun password benar.

## Catatan

- Pastikan waktu pada komputer Anda sudah tepat agar batas waktu 10 menit berfungsi dengan baik.

- https://chathast-fuukfsjmeyh3sxcp9ed7k4.streamlit.app/

