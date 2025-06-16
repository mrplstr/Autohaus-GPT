import streamlit as st
import json
import hashlib
import os

from gpt_manager import load_gpts, add_gpt, delete_gpt

USERS_FILE = "data/users.json"

# --------- Login-Funktionen ----------
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
                st.rerun()
            else:
                st.error("Falscher Benutzername oder Passwort")

def logout():
    if "user" in st.session_state:
        if st.sidebar.button("🚪 Logout"):
            del st.session_state["user"]
            st.rerun()

def is_logged_in():
    return "user" in st.session_state

def get_current_user():
    return st.session_state.get("user", None)

# --------- App ---------
st.set_page_config(page_title="Autohaus GPT", layout="wide")

if not is_logged_in():
    login()
else:
    user = get_current_user()
    st.sidebar.markdown(f"👤 Eingeloggt als: `{user['username']}` ({user['role']})")
    logout()

    st.title("🚗 Autohaus GPT")

    if user["role"] == "admin":
        st.subheader("🛠 Adminbereich – GPT-Verwaltung")

        # GPT-Erstellung
        with st.expander("➕ Neuen GPT erstellen"):
            name = st.text_input("Name")
            system_prompt = st.text_area("System-Prompt", height=150)
            temperature = st.slider("Temperatur", 0.0, 1.0, 0.7)
            max_tokens = st.number_input("Max Tokens", min_value=100, max_value=4000, value=800)

            if st.button("GPT hinzufügen"):
                if name and system_prompt:
                    add_gpt(name, system_prompt, temperature, max_tokens)
                    st.success(f"{name} wurde gespeichert.")
                    st.rerun()
                else:
                    st.error("Bitte Name und Prompt angeben.")

        # GPT-Liste anzeigen
        st.subheader("🗂️ Vorhandene GPTs")
        gpts = load_gpts()
        if gpts:
            for gpt in gpts:
                with st.container():
                    st.markdown(f"**{gpt['name']}** (ID: {gpt['id']})")
                    st.code(gpt['system_prompt'], language="markdown")
                    cols = st.columns(3)
                    cols[0].markdown(f"🌡️ Temperatur: `{gpt['temperature']}`")
                    cols[1].markdown(f"📏 Max Tokens: `{gpt['max_tokens']}`")
                    if cols[2].button("🗑️ Löschen", key=f"del_{gpt['id']}"):
                        delete_gpt(gpt['id'])
                        st.warning(f"{gpt['name']} wurde gelöscht.")
                        st.rerun()
        else:
            st.info("Noch keine GPTs erstellt.")

    elif user["role"] == "user":
        st.subheader("🤖 Meine GPTs")
        st.info("Hier wird bald dein GPT-Chat erscheinen.")

    else:
        st.warning("Unbekannte Rolle. Bitte kontaktiere den Administrator.")
