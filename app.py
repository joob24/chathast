import streamlit as st
import base64
import json
import time
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
        "timestamp": int(time.time()),
        "message": message
    }).encode()

    ct = aesgcm.encrypt(nonce, payload, None)
    encrypted = base64.b64encode(salt + nonce + ct).decode()
    return encrypted


def decrypt_message(encrypted_b64: str, password: str) -> str:
    try:
        data = base64.b64decode(encrypted_b64)
        salt = data[:16]
        nonce = data[16:28]
        ct = data[28:]

        key = derive_key(password, salt)
        aesgcm = AESGCM(key)
        decrypted = aesgcm.decrypt(nonce, ct, None)
        payload = json.loads(decrypted)

        timestamp = payload["timestamp"]
        message = payload["message"]

        if int(time.time()) - timestamp > 600:
            return "Pesan sudah kedaluwarsa dan tidak dapat dibaca."

        return message
    except:
        return "Password salah atau data pesan tidak valid."


# ==================== UI + DESAIN ====================

def main():
    st.set_page_config(page_title="Enkripsi & Dekripsi", layout="wide")

    # CSS & auto-expand JS
    st.markdown("""
    <style>
    body { font-family: 'Segoe UI', sans-serif; }

    .title-box {
        background: linear-gradient(90deg, #0d6efd, #6610f2);
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
    }

    .card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e6e6e6;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    textarea {
        border-radius: 8px !important;
        overflow-y: hidden !important;
        min-height: 120px !important;
        resize: none !important;
    }

    .stButton>button {
        background: #0d6efd !important;
        color: white !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        border: none !important;
        font-size: 16px !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover {
        background: #0b5ed7 !important;
        transform: scale(1.03);
    }
    </style>

    <script>
    // Auto expand all textarea in Streamlit
    const resizeTextAreas = () => {
        document.querySelectorAll("textarea").forEach(el => {
            el.style.height = "auto";
            el.style.height = (el.scrollHeight) + "px";
            el.addEventListener("input", () => {
                el.style.height = "auto";
                el.style.height = (el.scrollHeight) + "px";
            });
        });
    };

    window.addEventListener("load", resizeTextAreas);
    setTimeout(resizeTextAreas, 500);  // for widgets that load late
    </script>
    """, unsafe_allow_html=True)

    # Header
    st.markdown(
        "<div class='title-box'><h2>🔐 Joe Wevil - Enkripsi & Dekripsi Pesan</h2></div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # ======================== ENKRIPSI ========================
    with col1:
        st.markdown("<div class='card'><h3>🔒 Enkripsi Pesan</h3>", unsafe_allow_html=True)

        message = st.text_area("Masukkan pesan yang ingin dienkripsi:")
        password = st.text_input("Password (berlaku 10 menit):", type="password")

        if st.button("Enkripsi"):
            if not message or not password:
                st.warning("Pesan dan password harus diisi.")
            else:
                encrypted = encrypt_message(message, password)
                st.success("Pesan berhasil dienkripsi!")
                st.text_area("Hasil Enkripsi (bagikan ke penerima):", encrypted)

        st.markdown("</div>", unsafe_allow_html=True)

    # ======================== DEKRIPSI ========================
    with col2:
        st.markdown("<div class='card'><h3>🔓 Dekripsi Pesan</h3>", unsafe_allow_html=True)

        encrypted_data = st.text_area("Masukkan hash/enkripsi pesan:")
        password_dec = st.text_input("Password untuk membuka pesan:", type="password")

        if st.button("Dekripsi"):
            if not encrypted_data or not password_dec:
                st.warning("Hash dan password harus diisi.")
            else:
                decrypted = decrypt_message(encrypted_data, password_dec)
                if decrypted in [
                    "Password salah atau data pesan tidak valid.",
                    "Pesan sudah kedaluwarsa dan tidak dapat dibaca."
                ]:
                    st.error(decrypted)
                else:
                    st.success("Pesan berhasil didekripsi:")
                    st.text_area("", decrypted)

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
