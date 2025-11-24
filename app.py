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
.stApp {
    background: #f6f9fc;
    padding: 20px;
    font-family: "Segoe UI", sans-serif;
}
.custom-card {
    background: white;
    padding: 25px 30px;
    border-radius: 15px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}
textarea {
    overflow: hidden !important;
    min-height: 120px !important;
    resize: none !important;
}
textarea:focus, textarea:not(:placeholder-shown) {
    height: auto !important;
}
h1 {
    font-weight: 700;
    color: #1a3d7c;
}
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
.copy-btn {
    background: #1a73e8;
    color: white;
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    display: inline-block;
    margin-top: 5px;
}
.copy-btn:hover {
    background: #135cbc;
}
</style>

<script>
// Auto expand textarea
function autoExpand() {
    const textareas = document.querySelectorAll("textarea");
    textareas.forEach(t => {
        t.addEventListener('input', function() {
            this.style.height = "auto";
            this.style.height = (this.scrollHeight) + "px";
        });
        t.style.height = "auto";
        t.style.height = (t.scrollHeight) + "px";
    });
}
setTimeout(autoExpand, 500);

// Copy function
function copyToClipboard(textId) {
    const content = document.getElementById(textId).innerText;
    navigator.clipboard.writeText(content).then(function() {
        alert("Berhasil disalin ke clipboard!");
    });
}
</script>
""", unsafe_allow_html=True)


# --- TITLE ---
st.markdown("<h1 align='center'>🔐 Aplikasi Enkripsi & Deskripsi</h1>", unsafe_allow_html=True)
st.write("Masukkan pesan dan password untuk melakukan enkripsi atau deskripsi.")


# --- KEY GENERATOR ---
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


# --- ENKRIPSI ---
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

                # BLOCK HASIL + COPY
                unique_id = "encrypted_result"
                st.markdown(
                    f"""
                    <pre id="{unique_id}" style="padding:10px; background:#eef3ff; border-radius:8px;">{encrypted_text}</pre>
                    <div class="copy-btn" onclick="copyToClipboard('{unique_id}')">📋 Copy</div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Isi pesan dan password terlebih dahulu.")

    st.markdown("</div>", unsafe_allow_html=True)


# --- DESKRIPSI ---
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

                # BLOCK HASIL + COPY
                unique_id = "decrypted_result"
                st.markdown(
                    f"""
                    <pre id="{unique_id}" style="padding:10px; background:#eef3ff; border-radius:8px;">{decrypted_text}</pre>
                    <div class="copy-btn" onclick="copyToClipboard('{unique_id}')">📋 Copy</div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception:
                st.error("Password salah atau format enkripsi tidak valid.")
        else:
            st.warning("Isi pesan enkripsi dan password terlebih dahulu.")

    st.markdown("</div>", unsafe_allow_html=True)
