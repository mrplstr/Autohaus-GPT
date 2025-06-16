import streamlit as st
import json
import hashlib
import os

USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    if "user" not in st.session_state:
        st.sidebar.title("🔐 Login")
        username = st.sidebar.text_input("Benutzername")
        password = st.sidebar.text_input("Passwort", type="password")
        if st.sidebar.button("Einloggen"):
            users = load_users()
            hashed = hash_password(password)
            matched_user = next((u for u in users if u["username"] == username and u["password"] == hashed), None)

            if matched_user:
                st.session_state["user"] = {
                    "id": matched_user["id"],
                    "username": matched_user["username"],
                    "role": matched_user["role"]
                }
                st.success(f"Willkommen, {matched_user['username']} 👋")
                st.experimental_set_query_params(logged_in="1")  # Triggered reload
            else:
                st.error("Falscher Benutzername oder Passwort")

def logout():
    if "user" in st.session_state:
        if st.sidebar.button("🚪 Logout"):
            del st.session_state["user"]
            st.experimental_set_query_params()  # Reset URL params

def is_logged_in():
    return "user" in st.session_state

def get_current_user():
    return st.session_state.get("user", None)
