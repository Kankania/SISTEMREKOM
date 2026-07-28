import streamlit as st
import pandas as pd
import os
import shutil
from auth import login, logout

# ===========================
# LOGIN
# ===========================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    login()
    st.stop()

# ===========================
# DASHBOARD
# ===========================
st.title("Dashboard Admin")
st.success("Selamat datang, Admin!")

# Membaca data
df = pd.read_excel("data_buah.xlsx")

# Hapus kolom yang tidak diperlukan jika ada
df = df.drop(columns=["Karbohidrat", "Serat"], errors="ignore")

# Simpan kembali agar Excel ikut bersih
df.to_excel("data_buah.xlsx", index=False)

st.subheader("Data Buah")

st.dataframe(df, use_container_width=True)

st.divider()
st.subheader("Tambah Data Buah")

with st.form("tambah_buah"):

    nama = st.text_input("Nama Buah")
    karbo = st.number_input("Karbohidrat (g)", min_value=0.0, step=0.1)
    serat = st.number_input("Serat (g)", min_value=0.0, step=0.1)
    berat = st.number_input("Berat (g)", min_value=0.0, step=0.1)
    jumlah_potongan = st.number_input("Jumlah Potongan", min_value=0.0, step=0.1)
    keterangan_potongan = st.text_input("Keterangan Potongan")

    simpan = st.form_submit_button("Simpan")

    if simpan:

        data_baru = pd.DataFrame({
            "Nama Buah":[nama],
            "Karbohidrat (g)":[karbo],
            "Serat (g)":[serat],
            "Berat (g)":[berat],
            "Jumlah Potongan":[jumlah_potongan],
            "Keterangan Potongan":[keterangan_potongan]
        })

        df = pd.concat([df, data_baru], ignore_index=True)

        df.to_excel("data_buah.xlsx", index=False)

        st.success("Data berhasil ditambahkan.")

        st.rerun()

st.divider()
st.subheader("Edit Data Buah")

nama_edit = st.selectbox(
    "Pilih buah yang akan diedit",
    df["Nama Buah"]
)

index = df[df["Nama Buah"] == nama_edit].index[0]

with st.form("edit_data"):

    nama_baru = st.text_input(
        "Nama Buah",
        value=df.loc[index, "Nama Buah"]
    )

    karbo_edit = st.number_input(
        "Karbohidrat (g)",
        value=float(df.loc[index, "Karbohidrat (g)"]),
        step=0.1
    )

    serat_edit = st.number_input(
        "Serat (g)",
        value=float(df.loc[index, "Serat (g)"]),
        step=0.1
    )

    berat_edit = st.number_input(
        "Berat (g)",
        value=float(df.loc[index, "Berat (g)"]),
        step=0.1
    )
    jumlah_potongan_edit = st.number_input(
        "Jumlah Potongan",
        value=float(df.loc[index, "Jumlah Potongan"]),
        step=0.1
    )

    keterangan = st.text_input(
        "Keterangan Potongan",
        value=df.loc[index, "Keterangan Potongan"]
    )

    
    update = st.form_submit_button("Update")

    if update:

        df.loc[index, "Nama Buah"] = nama_baru
        df.loc[index, "Karbohidrat (g)"] = karbo_edit
        df.loc[index, "Serat (g)"] = serat_edit
        df.loc[index, "Berat (g)"] = berat_edit
        df.loc[index, "Jumlah Potongan"] = jumlah_potongan_edit
        df.loc[index, "Keterangan Potongan"] = keterangan

        df.to_excel("data_buah.xlsx", index=False)

        st.success("Data berhasil diperbarui.")

        st.rerun()

st.divider()
st.subheader("Hapus Data Buah")

hapus = st.selectbox(
    "Pilih buah yang akan dihapus",
    df["Nama Buah"],
    key="hapus"
)

if st.button("Hapus Data"):

    df = df[df["Nama Buah"] != hapus]

    df.to_excel("data_buah.xlsx", index=False)

    st.success("Data berhasil dihapus.")

    st.rerun()

st.divider()
st.subheader("Upload Foto Buah")

buah_foto = st.selectbox(
    "Pilih buah",
    df["Nama Buah"],
    key="foto"
)

uploaded = st.file_uploader(
    "Pilih foto",
    type=["png", "jpg", "jpeg", "svg"]
)

if st.button("Simpan Foto"):

    if uploaded is None:
        st.warning("Silakan pilih foto terlebih dahulu.")

    else:

        # nama file sesuai nama upload
        nama_file = uploaded.name

        # lokasi penyimpanan
        path_simpan = os.path.join("assets", nama_file)

        # simpan file ke folder assets
        with open(path_simpan, "wb") as f:
            f.write(uploaded.getbuffer())

        # update kolom Foto di Excel
        index = df[df["Nama Buah"] == buah_foto].index[0]

        df.loc[index, "Foto"] = nama_file

        df.to_excel("data_buah.xlsx", index=False)

        st.success("Foto berhasil diupload.")

        st.rerun()

st.write(f"Jumlah data buah : **{len(df)}**")

st.divider()

if st.button("Logout"):
    logout()