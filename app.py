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

# ==================== FUNGSI ====================

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_message(message: str, password: str) -> str:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)

    payload = json.dumps({
        'timestamp': int(time.time()),
        'message': message
    }).encode()

    ct = aesgcm.encrypt(nonce, payload, None)
    encrypted_data = base64.b64encode(salt + nonce + ct).decode()
    return encrypted_data

def decrypt_message(encrypted_data_b64: str, password: str) -> str:
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

        if int(time.time()) - timestamp > 600:
            return "Pesan sudah kedaluwarsa dan tidak dapat dibaca."
        return message

    except:
        return "Password salah atau data pesan tidak valid."

# ==================== UI + DESAIN ====================

def main():
    st.set_page_config(page_title="Enkripsi & Dekripsi", layout="wide")

    # ---------- Custom CSS ----------
    st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
    }

    .title-box {
        background: linear-gradient(90deg, #0d6efd, #6610f2);
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0px
