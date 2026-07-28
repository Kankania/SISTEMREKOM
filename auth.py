import streamlit as st

USERNAME = "admin"
PASSWORD = "admin123"

def login():
    st.title("Login Admin")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state["login"] = True
            st.success("Login berhasil")
            st.rerun()
        else:
            st.error("Username atau Password salah")


def logout():
    st.session_state["login"] = False
    st.rerun()