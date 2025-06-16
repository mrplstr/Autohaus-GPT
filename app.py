import streamlit as st
from auth import login, logout, is_logged_in, get_current_user
from gpt_manager import load_gpts, add_gpt, delete_gpt

st.set_page_config(page_title="Autohaus GPT", layout="wide")

def main():
    if not is_logged_in():
        login()
    else:
        user = get_current_user()

        # Sidebar
        st.sidebar.markdown(f"👤 Eingeloggt als: `{user['username']}` ({user['role']})")
        logout()

        # Hauptbereich
        st.title("🚗 Autohaus GPT")

        if user["role"] == "admin":
            st.subheader("🛠 Adminbereich – GPT-Verwaltung")

            # GPT-Erstellungsformular
            with st.expander("➕ Neuen GPT erstellen"):
                name = st.text_input("Name")
                system_prompt = st.text_area("System-Prompt", height=150)
                temperature = st.slider("Temperatur", 0.0, 1.0, 0.7)
                max_tokens = st.number_input("Max Tokens", min_value=100, max_value=4000, value=800)

                if st.button("GPT hinzufügen"):
                    if name and system_prompt:
                        add_gpt(name, system_prompt, temperature, max_tokens)
                        st.success(f"{name} wurde gespeichert.")
                        st.experimental_rerun()
                    else:
                        st.error("Bitte Name und Prompt angeben.")

            # Bestehende GPTs anzeigen
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
                            st.experimental_rerun()
            else:
                st.info("Noch keine GPTs erstellt.")

        elif user["role"] == "user":
            st.subheader("🤖 Meine GPTs")
            st.info("In Kürze kannst du hier mit deinen GPTs chatten.")

        else:
            st.warning("Unbekannte Rolle. Bitte kontaktiere den Administrator.")

if __name__ == "__main__":
    main()
