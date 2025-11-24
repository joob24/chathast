import streamlit as st
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
from html import escape as html_escape
import streamlit.components.v1 as components

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
</style>
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


def render_copy_block(content: str, uid: str, height: int = 140):
    """
    Render a styled pre block with a Copy button using st.components.v1.html.
    Uses html escaping for the content.
    """
    safe = html_escape(content)
    html_code = f"""
    <div style="font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto; background:#eef3ff; padding:12px; border-radius:8px;">
      <pre id="{uid}" style="white-space:pre-wrap; word-wrap:break-word; margin:0; font-size:13px;">{safe}</pre>
      <div style="margin-top:8px; display:flex; gap:8px;">
        <button id="{uid}_btn" style="background:#1a73e8; color:white; border:none; padding:8px 12px; border-radius:6px; cursor:pointer;">📋 Copy</button>
        <span id="{uid}_msg" style="align-self:center; color:#0b3a80; font-size:13px;"></span>
      </div>
    </div>

    <script>
    const btn = document.getElementById("{uid}_btn");
    const msg = document.getElementById("{uid}_msg");
    btn.addEventListener("click", async function() {{
        try {{
            const text = document.getElementById("{uid}").innerText;
            // Try navigator clipboard first
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                await navigator.clipboard.writeText(text);
            }} else {{
                // Fallback: create textarea
                const ta = document.createElement('textarea');
                ta.value = text;
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
            }}
            msg.innerText = "Disalin!";
            setTimeout(()=> msg.innerText = "", 1800);
        }} catch (err) {{
            console.error(err);
            msg.innerText = "Gagal menyalin";
            setTimeout(()=> msg.innerText = "", 2200);
        }}
    }});
    </script>
    """
    # components.html allows the JS to run within an iframe; height must accommodate content
    components.html(html_code, height=height, scrolling=True)


# --- ENKRIPSI ---
with st.container():
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.subheader("🔒 Enkripsi Pesan")

    text_encrypt = st.text_area("Masukkan Pesan untuk Enkripsi:", placeholder="Tulis pesan...", key="encrypt_area")
    password_encrypt = st.text_input("Masukkan Password:", type="password", key="pw_encrypt")

    if st.button("Enkripsi Pesan"):
        if text_encrypt and password_encrypt:
            try:
                key = generate_key(password_encrypt)
                cipher = Fernet(key)
                encrypted_text = cipher.encrypt(text_encrypt.encode()).decode()

                st.success("Pesan berhasil dienkripsi:")
                # render copy block with unique id
                render_copy_block(encrypted_text, uid="encrypted_result", height=160)

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
                render_copy_block(decrypted_text, uid="decrypted_result", height=160)

            except Exception:
                st.error("Password salah atau format enkripsi tidak valid.")
        else:
            st.warning("Isi pesan enkripsi dan password terlebih dahulu.")

    st.markdown("</div>", unsafe_allow_html=True)
