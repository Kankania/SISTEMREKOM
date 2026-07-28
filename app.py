import streamlit as st
import base64

st.set_page_config(
    page_title="NutriMatch",
    layout="wide"
)

# LOAD CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# BACKGROUND
def set_bg(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background:
            linear-gradient(
                rgba(0, 0, 0, 0),
                rgba(0, 0, 0, 0)
            ),
            url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)
set_bg("assets/bgr.png")

# =========================
# CENTER WRAPPER FIX
# =========================

st.markdown('<div class="center-container">', unsafe_allow_html=True)

# LOGO CENTER
def img_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = img_to_base64("assets/logo.png")

st.markdown(f"""
<div style="display:flex; justify-content:center; margin-bottom:20px;">
    <img src="data:image/png;base64,{logo_base64}" width="170">
</div>
""", unsafe_allow_html=True)

# HERO BOX
st.markdown("""
<div class="hero-box">
    <h3>Sahabat Buah Sehat Anda</h3>
    <p>Temukan kombinasi terbaik dengan porsi tepat tanpa khawatir lonjakan gula darah</p>
</div>
""", unsafe_allow_html=True)

# BUTTON CENTER

st.markdown('<div class="button-wrapper">', unsafe_allow_html=True)

if st.button("Mulai", key="green", type="primary"):
    st.switch_page("pages/1pilihbuah.py")

st.markdown('</div>', unsafe_allow_html=True)