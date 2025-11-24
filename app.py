import streamlit as st
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Enkripsi & Deskripsi | Professional App",
    layout="centered"
)

# --- CUSTOM CSS INCLUDING AUTO-EXPAND TEXTAREA ---
st.markdown("""
<style>
/* Modern container style */
.stApp {
    background: #f6f9fc;
    padding: 20px;
    font-family: "Segoe UI", sans-serif;
}

/* Card styling */
.custom-card {
    background: white;
    padding: 25px 30px;
    border-radius: 15px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* Auto-expand textarea */
textarea {
    overflow: hidden !important;
    min-height: 120px !important;
    resize: none !important;
}

/* Increase height dynamically */
textarea:focus, textarea:not(:placeholder-shown) {
    height: auto !important;
}

/* Title styling */
h1 {
    font-weight: 700;
    color: #1a3d7c;
}

/* Button styling */
.stButton button {
    background: #1a73e8;
    color: white;
    border-radius: 8px;
    padding: 10px 18px;
    border: none;
}
.stButton button:hover {
    background: #135cbc;
}
</style>

<script>
// Auto expand all textareas
function autoExpand() {
    const textareas = document.querySelectorAll("textarea");
    textareas.forEach(t => {
        t.addEventListener('input', function() {
            this.style.height = "auto";
            this.style.height = (this.scrollHeight) + "px";
        });
        // auto initial expand
        t.style.height = "auto";
        t.style.height = (t.scrollHeight) + "px";
    });
}

setTimeout(autoExpand, 500);
</script>
""", unsafe_allow_html=True)

# --- TITLE ---
st.markdown("<h1 align='center'>🔐 Aplikasi Enkripsi & Deskripsi</h1>", unsafe_allow_html=True)
st.write("Masukkan pesan dan password untuk melakukan enkripsi atau deskripsi.")

# --- KEY DERIVATION FUNCTION ---
def generate_key(password: str) -> bytes:
    password_bytes = password.encode()
    salt = b"static_salt_value_123"
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password_bytes))

# --- CARD (ENKRIPSI) ---
with st.container():
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.subheader("🔒 Enkripsi Pesan")

    text_encrypt = st.text_area("Masukkan Pesan untuk Enkripsi:", placeholder="Tulis pesan...", key="encrypt_area")
    password_encrypt = st.text_input("Masukkan Password:", type="password")

    if st.button("Enkripsi Pesan"):
        if text_encrypt and password_encrypt:
            try:
                key = generate_key(password_encrypt)
                cipher = Fernet(key)
                encrypted_text = cipher.encrypt(text_encrypt.encode()).decode()
                st.success("Pesan berhasil dienkripsi:")
                st.code(encrypted_text)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Isi pesan dan password terlebih dahulu.")

    st.markdown("</div>", unsafe_allow_html=True)

# --- CARD (DESKRIPSI) ---
with st.container():
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.subheader("🔓 Deskripsi Pesan")

    text_decrypt = st.text_area("Masukkan Pesan Enkripsi:", placeholder="Tempel hasil enkripsi...", key="decrypt_area")
    password_decrypt = st.text_input("Masukkan Password:", type="password", key="pw2")

    if st.button("Deskripsi Pesan"):
        if text_decrypt and password_decrypt:
            try:
                key = generate_key(password_decrypt)
                cipher = Fernet(key)
                decrypted_text = cipher.decrypt(text_decrypt.encode()).decode()
                st.success("Pesan berhasil didekripsi:")
                st.code(decrypted_text)
            except Exception as e:
                st.error("Password salah atau format enkripsi tidak valid.")
        else:
            st.warning("Isi pesan enkripsi dan password terlebih dahulu.")

    st.markdown("</div>", unsafe_allow_html=True)
