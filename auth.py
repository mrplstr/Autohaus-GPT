import streamlit as st
import json
import hashlib

def load_users():
    with open("data/users.json", "r") as f:
        return json.load(f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    if "user" not in st.session_state:
        st.sidebar.title("🔐 Login")
        users = load_users()
        username = st.sidebar.text_input("Benutzername")
        password = st.sidebar.text_input("Passwort", type="password")

        if st.sidebar.button("Einloggen"):
            pw_hash = hash_password(password)
            for user in users:
                if user["username"] == username and user["password"] == pw_hash:
                    st.session_state["user"] = {
                        "id": user["id"],
                        "username": user["username"],
                        "role": user["role"]
                    }
                    st.success(f"Willkommen, {user['username']} 👋")
                    st.experimental_rerun()
            st.error("Falscher Benutzername oder Passwort")

def logout():
    if "user" in st.session_state:
        st.sidebar.button("🚪 Logout", on_click=lambda: st.session_state.pop("user"))

def is_logged_in():
    return "user" in st.session_state

def get_current_user():
    return st.session_state.get("user", None)
