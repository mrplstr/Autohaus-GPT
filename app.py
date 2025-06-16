import streamlit as st
from auth import login, logout, is_logged_in, get_current_user

st.set_page_config(page_title="Autohaus GPT", layout="wide")

# Hauptlogik
def main():
    if not is_logged_in():
        login()
    else:
        user = get_current_user()

        # Sidebar-Infos
        st.sidebar.markdown(f"👤 Eingeloggt als: `{user['username']}` ({user['role']})")
        logout()

        # Hauptbereich
        st.title("🚗 Autohaus GPT")

        if user["role"] == "admin":
            st.subheader("🛠 Adminbereich")
            st.write("Hier kannst du GPTs verwalten, Benutzer zuweisen und Einstellungen vornehmen.")
            st.info("Dieser Bereich wird im nächsten Schritt erweitert.")

        elif user["role"] == "user":
            st.subheader("🤖 Meine GPTs")
            st.write("Hier siehst du deine freigegebenen GPTs.")
            st.info("In Kürze kannst du hier mit deinen GPTs chatten.")

        else:
            st.warning("Unbekannte Rolle. Bitte kontaktiere den Administrator.")

if __name__ == "__main__":
    main()
