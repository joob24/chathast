import streamlit as st
import base64
import json
import time
from datetime import datetime, timezone
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import os

def derive_key(password: str, salt: bytes) -> bytes:
    """Turunkan kunci enkripsi dari password menggunakan PBKDF2HMAC."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

def encrypt_message(message: str, password: str) -> str:
    """
    Enkripsi pesan dengan password dan masukkan timestamp.
    Mengembalikan hasil enkripsi dalam format base64 string.
    """
    salt = os.urandom(16)  # Salt acak untuk KDF
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # Nonce acak untuk AES GCM

    # Buat payload dengan pesan dan timestamp (waktu UTC sekarang dalam detik)
    timestamp = int(time.time())
    payload = json.dumps({
        'timestamp': timestamp,
        'message': message
    }).encode()

    ct = aesgcm.encrypt(nonce, payload, None)

    # Gabungkan salt, nonce, dan ciphertext lalu encode base64
    encrypted_data = base64.b64encode(salt + nonce + ct).decode()
    return encrypted_data

def decrypt_message(encrypted_data_b64: str, password: str) -> str:
    """
    Dekripsi pesan dengan password.
    Jika password salah atau pesan sudah lewat 10 menit tidak bisa dibaca.
    """
    try:
        data = base64.b64decode(encrypted_data_b64)
        salt = data[:16]
        nonce = data[16:28]
        ct = data[28:]
        key = derive_key(password, salt)
        aesgcm = AESGCM(key)
        decrypted_payload = aesgcm.decrypt(nonce, ct, None)
        payload = json.loads(decrypted_payload)

        timestamp = payload.get('timestamp')
        message = payload.get('message')
        current_time = int(time.time())

        # Periksa apakah pesan masih valid dalam 10 menit (600 detik)
        if current_time - timestamp > 600:
            return "Pesan sudah kedaluwarsa dan tidak dapat dibaca."
        else:
            return message
    except Exception as e:
        return "Password salah atau data pesan tidak valid."

def main():
    st.title("Aplikasi Enkripsi Pesan dengan Password Berjangka Waktu")

    menu = ["Enkripsi Pesan", "Dekripsi Pesan"]
    choice = st.sidebar.selectbox("Pilih Fitur", menu)

    if choice == "Enkripsi Pesan":
        st.header("Fitur 1: Enkripsi Pesan")
        message = st.text_area("Masukkan pesan yang ingin dienkripsi:")
        password = st.text_input("Masukkan password (berlaku 10 menit):", type="password")
        if st.button("Enkripsi"):
            if not message or not password:
                st.warning("Pesan dan password harus diisi.")
            else:
                encrypted = encrypt_message(message, password)
                st.success("Pesan berhasil dienkripsi!")
                st.text_area("Hash/enkripsi pesan (bagikan ini ke penerima):", encrypted, height=150)

    elif choice == "Dekripsi Pesan":
        st.header("Fitur 2: Dekripsi Pesan")
        encrypted = st.text_area("Masukkan hash/enkripsi pesan:")
        password = st.text_input("Masukkan password untuk membuka pesan:", type="password")
        if st.button("Dekripsi"):
            if not encrypted or not password:
                st.warning("Hash pesan dan password harus diisi.")
            else:
                decrypted = decrypt_message(encrypted, password)
                if decrypted == "Password salah atau data pesan tidak valid." or decrypted == "Pesan sudah kedaluwarsa dan tidak dapat dibaca.":
                    st.error(decrypted)
                else:
                    st.success("Pesan berhasil didekripsi:")
                    st.write(decrypted)

if __name__ == "__main__":
    main()
