import streamlit as st
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
from html import escape as html_escape
import streamlit.components.v1 as components

# PAGE CONFIG
st.set_page_config(
    page_title="Enkripsi & Deskripsi | Professional App",
    layout="centered"
)

# MOBILE-FRIENDLY CSS
st.markdown("""
<style>

/* GLOBAL MOBILE SETTINGS */
html, body, .stApp {
    max-width: 100% !important;
    overflow-x: hidden !important;
}

.stApp {
    background: #f6f9fc;
    padding: 10px;
    font-family: "Segoe UI", sans-serif;
}

/* CARD */
.custom-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 25px;
    width: 100%;
}

/* TITLE */
h1 {
    font-weight: 700;
    color: #1a3d7c;
    text-align: center;
    font-size: 26px;
}

/* MOBILE TITLE ADJUST */
@media (max-width: 480px) {
    h1 {
        font-size: 22px;
    }
}

/* TEXTAREA */
textarea {
    overflow: hidden !important;
    min-height: 120px !important;
    resize: none !important;
    width: 100% !important;
    font-size: 15px !important;
}

/* BUTTON */
.stButton button {
    background: #1a73e8;
    color: white;
    border-radius: 10px;
    padding: 12px 20px;
    width: 100%;
    font-size: 16px;
    border: none;
}
.stButton button:hover {
    background: #135cbc;
}

/* COPY BLOCK MOBILE OPTIMIZATION */
.copy-box {
    background:#eef3ff; 
    padding:12px; 
    border-radius:8px;
}
.copy-box pre {
    white-space:pre-wrap; 
    word-wrap:break-word; 
    margin:0; 
    font-size:14px;
}

/* MOBILE BUTTON INLINE FIX */
.copy-btn-container {
    margin-top:8px; 
    display:flex; 
    gap:8px;
    width: 100%;
}
.copy-btn-container button {
    flex: 1;
    padding:10px;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)



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



# --- COPY BLOCK ---
def render_copy_block(content: str, uid: str, height: int = 160):

    safe = html_escape(content)
    html_code = f"""
    <div class="copy-box">
      <pre id="{uid}">{safe}</pre>

      <div class="copy-btn-container">
        <button id="{uid}_btn" style="background:#1a73e8; color:white; border:none; border-radius:6px; cursor:pointer;">📋 Copy</button>
        <span id="{uid}_msg" style="align-self:center; color:#0b3a80; font-size:13px;"></span>
      </div>
    </div>

    <script>
    const btn = document.getElementById("{uid}_btn");
    const msg = document.getElementById("{uid}_msg");

    btn.addEventListener("click", async function() {{
        try {{
            const text = document.getElementById("{uid}").innerText;
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                await navigator.clipboard.writeText(text);
            }} else {{
                const ta = document.createElement('textarea');
                ta.value = text;
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                ta.remove();
            }}
            msg.innerText = "Disalin!";
            setTimeout(()=> msg.innerText = "", 1500);
        }} catch (err) {{
            msg.innerText = "Gagal menyalin";
            setTimeout(()=> msg.innerText = "", 2000);
        }}
    }});
    </script>
    """

    components.html(html_code, height=height, scrolling=False)




# ------------------------------------------------------------------------
# ENKRIPSI
# ------------------------------------------------------------------------
with st.container():
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:20px; font-weight:700; margin-bottom:10px;">
    🔒 Enkripsi Pesan
    </div>
    """, unsafe_allow_html=True)

    text_encrypt = st.text_area("Masukkan Pesan untuk Enkripsi:", 
                                placeholder="Tulis pesan...", 
                                key="encrypt_area")

    password_encrypt = st.text_input("Masukkan Password:", 
                                     type="password", 
                                     key="pw_encrypt")

    if st.button("Enkripsi Pesan"):
        if text_encrypt and password_encrypt:
            try:
                key = generate_key(password_encrypt)
                cipher = Fernet(key)
                encrypted_text = cipher.encrypt(text_encrypt.encode()).decode()

                st.success("Pesan berhasil dienkripsi:")
                render_copy_block(encrypted_text, uid="encrypted_result", height=180)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Isi pesan dan password terlebih dahulu.")

    st.markdown("</div>", unsafe_allow_html=True)




# ------------------------------------------------------------------------
# DESKRIPSI
# ------------------------------------------------------------------------
with st.container():
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:20px; font-weight:700; margin-bottom:10px;">
    🔓 Deskripsi Pesan
    </div>
    """, unsafe_allow_html=True)

    text_decrypt = st.text_area("Masukkan Pesan Enkripsi:", 
                                placeholder="Tempel hasil enkripsi...", 
                                key="decrypt_area")

    password_decrypt = st.text_input("Masukkan Password:", 
                                     type="password", 
                                     key="pw2")

    if st.button("Deskripsi Pesan"):
        if text_decrypt and password_decrypt:
            try:
                key = generate_key(password_decrypt)
                cipher = Fernet(key)
                decrypted_text = cipher.decrypt(text_decrypt.encode()).decode()

                st.success("Pesan berhasil didekripsi:")
                render_copy_block(decrypted_text, uid="decrypted_result", height=180)

            except Exception:
                st.error("Password salah atau format enkripsi tidak valid.")
        else:
            st.warning("Isi pesan enkripsi dan password terlebih dahulu.")

    st.markdown("</div>", unsafe_allow_html=True)

 st.markdown("---")
    st.markdown(
        """
        joe wevil - development python streamlit\n
   
        """
    )



