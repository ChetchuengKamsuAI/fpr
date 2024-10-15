import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="EcoTrace - Connexion", page_icon="🌍", layout="centered")

# Fonction pour afficher les enregistrements d'une table spécifique dans un tableau responsive
def afficher_enregistrements(table, conn):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table}')
    enregistrements = cursor.fetchall()
    colonnes = [description[0] for description in cursor.description]  # Récupération des noms de colonnes
    
    st.subheader(f"📋 Enregistrements de la table {table}")
    if enregistrements:
        df = pd.DataFrame(enregistrements, columns=colonnes)
        st.dataframe(df, use_container_width=True)  # Tableau responsive
    else:
        st.write(f"Aucun enregistrement dans la table {table}.")

# Fonction pour ajouter un enregistrement dans une table
def ajouter_enregistrement(table, conn, colonnes, valeurs):
    cursor = conn.cursor()
    query = f'INSERT INTO {table} ({", ".join(colonnes)}) VALUES ({", ".join(["?" for _ in valeurs])})'
    cursor.execute(query, valeurs)
    conn.commit()
    st.success(f"Enregistrement ajouté avec succès dans la table {table}.")

# Fonction pour supprimer un enregistrement par ID
def supprimer_enregistrement(table, conn, id_colonne, id_valeur):
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {table} WHERE {id_colonne}=?', (id_valeur,))
    conn.commit()
    st.success(f"Enregistrement avec ID {id_valeur} supprimé de la table {table}.")

# Interface d'administration
def admin_page():
    st.title("🛠️ Page d'administration")
    
    # Sélection de la base de données
    db_choice = st.sidebar.selectbox("Sélectionnez la base de données", ["ecotrace.db", "users.db"])
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_choice)
    
    # Sélection de la table
    if db_choice == "ecotrace.db":
        table_choice = st.sidebar.selectbox("Sélectionnez la table", ["collecte_dechets", "rewards"])
    elif db_choice == "users.db":
        table_choice = st.sidebar.selectbox("Sélectionnez la table", ["users"])

    # Afficher les enregistrements de la table sélectionnée
    afficher_enregistrements(table_choice, conn)

    # Formulaire d'ajout d'enregistrement
    st.subheader(f"➕ Ajouter un enregistrement à la table {table_choice}")
    
    if table_choice == "collecte_dechets":
        zone = st.text_input("Zone")
        type_dechets = st.text_input("Type de déchets")
        quantite_kg = st.number_input("Quantité (kg)", min_value=0.0, step=0.1)
        progres_percent = st.number_input("Progression (%)", min_value=0, max_value=100)
        latitude = st.number_input("Latitude")
        longitude = st.number_input("Longitude")
        image_url = st.text_input("URL de l'image")
        
        if st.button("Ajouter un enregistrement"):
            ajouter_enregistrement("collecte_dechets", conn, 
                                   ["zone", "type_dechets", "quantite_kg", "progres_percent", "latitude", "longitude", "image_url"], 
                                   [zone, type_dechets, quantite_kg, progres_percent, latitude, longitude, image_url])

    elif table_choice == "rewards":
        utilisateur = st.text_input("Nom de l'utilisateur")
        points = st.number_input("Points", min_value=0)
        description = st.text_input("Description")
        montant_fcfa = st.number_input("Montant (FCFA)", min_value=0.0, step=100.0)
        
        if st.button("Ajouter un enregistrement"):
            ajouter_enregistrement("rewards", conn, 
                                   ["utilisateur", "points", "description", "montant_fcfa"], 
                                   [utilisateur, points, description, montant_fcfa])

    elif table_choice == "users":
        numero_telephone = st.text_input("Numéro de téléphone")
        nom_utilisateur = st.text_input("Nom d'utilisateur")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        
        if st.button("Ajouter un enregistrement"):
            ajouter_enregistrement("users", conn, 
                                   ["telephone", "username", "password"], 
                                   [numero_telephone, nom_utilisateur, mot_de_passe])

    # Formulaire de suppression d'enregistrement
    st.subheader(f"🗑️ Supprimer un enregistrement de la table {table_choice}")
    id_value = st.number_input(f"Entrez l'ID de l'enregistrement à supprimer", min_value=1, step=1)
    
    if st.button(f"Supprimer l'enregistrement ID {id_value}"):
        if table_choice == "collecte_dechets":
            supprimer_enregistrement("collecte_dechets", conn, "id", id_value)
        elif table_choice == "rewards":
            supprimer_enregistrement("rewards", conn, "id", id_value)
        elif table_choice == "users":
            supprimer_enregistrement("users", conn, "id", id_value)

    conn.close()

# Appel de la fonction admin_page pour exécuter l'interface d'administration
admin_page()
