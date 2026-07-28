import streamlit as st
import base64
import pandas as pd
import os

# =====================================
# CONFIG
# =====================================
st.set_page_config(
    page_title="Pilih Buah",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# LOAD CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
# SESSION STATE
# =====================================
if "selected_fruits" not in st.session_state:
    st.session_state.selected_fruits = []

# =====================================
# DATA
# =====================================
# =====================================
# DATA DARI EXCEL
# =====================================
df = pd.read_excel("data_buah.xlsx")

fruits = []

for _, row in df.iterrows():

    img = os.path.join("assets", row["Foto"])

    # Jika file tidak ditemukan gunakan gambar default
    if not os.path.exists(img):
        img = "assets/default.png"

    fruits.append({
        "name": row["Nama Buah"],
        "img": img
    })

# =====================================
# SELECT FUNCTION
# =====================================
def select_fruit(name):
    if name in st.session_state.selected_fruits:
        st.session_state.selected_fruits.remove(name)
    else:
        if len(st.session_state.selected_fruits) < 5:
            st.session_state.selected_fruits.append(name)
        else:
            st.warning("Maksimal 5 buah!")

# =====================================
# CENTER CONTAINER
# =====================================
st.markdown('<div class="page-container">', unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.markdown("""
<div class="page-title">
    Buah apa yang anda punya hari ini?
</div>
""", unsafe_allow_html=True)

# =====================================
# GRID WRAPPER CENTER
# =====================================
st.markdown('<div class="fruit-grid">', unsafe_allow_html=True)

selected = st.session_state.selected_fruits

for i in range(0, len(fruits), 5):
    cols = st.columns(5, gap="small")

    for j in range(5):
        if i + j < len(fruits):
            fruit = fruits[i + j]

            with cols[j]:
                st.markdown('<div class="fruit-card">', unsafe_allow_html=True)

                st.image(fruit["img"], width=100)

                # Cek apakah buah sudah dipilih
                disabled = fruit["name"] in st.session_state.selected_fruits

                if st.button(
                    fruit["name"],
                    key=f"btn_{fruit['name']}",
                    disabled=disabled,
                    use_container_width=True
                ):
                    select_fruit(fruit["name"])
                    st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================
# SELECTED BOX
# =====================================

selected = st.session_state.get("selected_fruits", [])

if selected:

    with st.container(border=True):

        cols = st.columns(5)

        for i, fruit_name in enumerate(selected):
            fruit = next((f for f in fruits if f["name"] == fruit_name), None)

            if fruit:
                with cols[i]:

                    st.image(fruit["img"], width=80)

                    if st.button(
                        fruit_name,
                        key=f"selected_{fruit_name}",
                        use_container_width=True
                    ):
                        st.session_state.selected_fruits.remove(fruit_name)
                        st.rerun()

# =====================================
# PROSES BUTTON
# =====================================
st.write("")

col1, col2 = st.columns([8, 1])

with col2:
    if st.button("Proses", type="primary", use_container_width=True):
        if len(selected) == 0:
            st.warning("Pilih buah terlebih dahulu")
        elif len(selected) == 0:
            st.warning("Pilih buah terlebih dahulu")
        else:
            st.switch_page("pages/2hasil.py")

st.markdown('</div>', unsafe_allow_html=True)