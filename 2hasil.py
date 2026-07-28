import streamlit as st
from pathlib import Path
from fuzzyLogic import proses_fuzzy
import base64
import pandas as pd
import os

# =====================================
# CONFIG
# =====================================
st.set_page_config(
    page_title="Hasil Rekomendasi",
    layout="wide"
)

# =====================================
# LOAD CSS
# =====================================
css_path = Path(__file__).parent.parent / "assets" / "style.css"

with open(css_path) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
# =====================================
# BACKGROUND
# =====================================
def set_bg(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background:
            linear-gradient(
                rgba(255,255,255,0.82),
                rgba(255,255,255,0.82)
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
# =====================================
# SESSION
# =====================================
selected = st.session_state.get("selected_fruits", [])

# Membaca data tambahan dari Excel
df = pd.read_excel("data_buah.xlsx")

# =====================================
# FUZZY PROCESS
# =====================================
hasil_buah, rata_kelayakan, status_kombinasi, total_konsumsi = proses_fuzzy(selected)

# =====================================
# IMAGE PATH
# =====================================
df = pd.read_excel("data_buah.xlsx")

fruit_images = {}

for _, row in df.iterrows():

    img = os.path.join("assets", row["Foto"])

    if not os.path.exists(img):
        img = "assets/default.png"

    fruit_images[row["Nama Buah"]] = img

# =====================================
# MAIN LAYOUT
# =====================================
left, right = st.columns([1.1, 1])

# =====================================
# LEFT SIDE
# =====================================
with left:

    st.markdown(
        f"""
        
        <div class="hasil-title-box">
            Kombinasi {status_kombinasi}<br><br>
            Total Porsi ± {round(total_konsumsi)} gram per hari<br>
            maksimal dibagi 3 kali sebagai selingan!
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================
# RIGHT SIDE
# =====================================
with right:

    st.markdown(
        """
        <div class="green-box">
            Rekomendasi Takaran
        </div>
        """,
        unsafe_allow_html=True
    )

    # =================================
    # HASIL REKOMENDASI
    # =================================
    for item in hasil_buah:
        
        # Mengambil informasi ukuran dari Excel
        info = df[df["Nama Buah"] == item["buah"]].iloc[0]

        berat = info["Berat (g)"]
        jumlah_potongan = info["Jumlah Potongan"]
        keterangan = info["Keterangan Potongan"]

        # Menghitung estimasi jumlah potongan
        estimasi_potongan = round((item["rekomendasi"] / berat) * jumlah_potongan)

        # Supaya minimal tampil 1 jika rekomendasi > 0
        if item["rekomendasi"] > 0 and estimasi_potongan == 0:
            estimasi_potongan = 1

        img = fruit_images.get(item["buah"])

        col_img, col_text = st.columns([1, 4])
    
        # =========================
        # IMAGE
        # =========================
        with col_img:
            st.image(img, width=85)

        # =========================
        # TEXT
        # =========================
        with col_text:

            st.markdown(
                f"""
                <div class="fruit-title"> 
                <p>{item['buah']}
                </p>
        
                </div>

                <div class="fruit-text">
                    Karbohidrat:</span>
                        {item['karbohidrat']} g
                    <br>
                    Serat:</span>
                        {item['serat']} g
                    <br>
                    Kategori:</span>
                        {item['kategori']}
                    <br>
                    Rekomendasi Konsumsi:</span>
                        {item['rekomendasi']} gram
                    <br>
                    Estimasi Penyajian:</span>
                        ± {estimasi_potongan} {keterangan}

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<hr>", unsafe_allow_html=True)