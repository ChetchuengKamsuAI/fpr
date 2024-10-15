import streamlit as st
import sqlite3
import hashlib
import subprocess

# --- Connexion à la base de données ---
def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

def create_users_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL,
                      phone_number TEXT NOT NULL UNIQUE,
                      password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def add_user(username, phone_number, password):
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('INSERT INTO users (username, phone_number, password) VALUES (?, ?, ?)', 
                   (username, phone_number, hashed_password))
    conn.commit()
    conn.close()

def verify_user(phone_number, password):
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('SELECT * FROM users WHERE phone_number=? AND password=?', 
                   (phone_number, hashed_password))
    result = cursor.fetchone()
    conn.close()
    return result

# --- UI / UX amélioré avec Streamlit ---
def main():
    st.set_page_config(page_title="EcoTrace - Connexion", page_icon="🌍", layout="centered")
    
    # Configuration des styles et couleurs (vert et blanc)
    st.markdown(
        """
        <style>
        .main {
            background-color: #ffffff;
            color: #006400;
        }
        .stButton>button {
            background-color: #006400;
            color: white;
        }
        .stTextInput>div>div>input {
            border-color: #006400;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Structure de la page avec 2 colonnes (image à gauche, contenu à droite)
    col1, col2 = st.columns([1, 2])

    with col1:
        # Ajout de l'image sur la gauche
        st.image("https://th.bing.com/th/id/OIP.kXbM74etdhf7LW1DDHhwrAHaHa?rs=1&pid=ImgDetMain", caption="Bienvenue sur EcoTrace", use_column_width=True)

    with col2:
        # Titre principal
        st.title("Bienvenue sur EcoTrace 🌍")
        st.markdown("### Système de gestion des déchets recyclables")

        # Séparation en onglets pour la connexion et l'inscription
        tab1, tab2 = st.tabs(["Se connecter", "Créer un compte"])

        with tab1:
            st.subheader("Connexion")

            login_phone_number = st.text_input("Numéro de Téléphone")
            login_password = st.text_input("Mot de Passe", type="password")

            if st.button("Se Connecter"):
                # Vérifier si c'est l'administrateur
                if login_phone_number == "620705361" and login_password == "Admin@237":
                    st.success("Bienvenue Admin ! Redirection vers la page d'administration.")
                    # Lancer admin.py
                    subprocess.run(["streamlit", "run", "admin.py"])
                    st.stop()

                # Vérifier si c'est un utilisateur normal
                elif verify_user(login_phone_number, login_password):
                    st.success(f"Bienvenue, {login_phone_number} !")
                    st.session_state.logged_in = True  # Marque l'utilisateur comme connecté
                    # Lancer app.py pour les utilisateurs normaux
                    subprocess.run(["streamlit", "run", "app.py"])
                    st.stop()

                else:
                    st.error("Numéro de téléphone ou mot de passe incorrect.")

        with tab2:
            st.subheader("Créer un nouveau compte")

            # Champ pour le nom d'utilisateur lors de l'inscription
            new_username = st.text_input("Nom d'utilisateur")
            new_phone_number = st.text_input("Numéro de Téléphone (pour inscription)")
            new_password = st.text_input("Mot de Passe (pour inscription)", type="password")

            if st.button("S'inscrire"):
                if len(new_username) > 0 and len(new_phone_number) > 0 and len(new_password) > 0:
                    try:
                        add_user(new_username, new_phone_number, new_password)
                        st.success(f"Compte créé avec succès pour {new_username}. Veuillez vous connecter.")
                    except sqlite3.IntegrityError:
                        st.error("Ce numéro de téléphone existe déjà.")
                else:
                    st.error("Tous les champs sont obligatoires.")

# Exécution de l'application
if __name__ == "__main__":    
    create_users_table()  # Créer la table des utilisateurs si elle n'existe pas
    main()
