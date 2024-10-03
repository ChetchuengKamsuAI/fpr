import streamlit as st
from PIL import Image
import sqlite3
import requests
from twilio.rest import Client
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import folium
import time 
import smtplib
from email.mime.text import MIMEText
from streamlit_folium import folium_static
# Couleurs et style
st.set_page_config(page_title="EcoTrace", layout="wide", initial_sidebar_state="expanded")

#---------------------------------------------------------#

# Fonction pour récupérer les actualités via l'API Mediastack en fonction d'un mot-clé
def get_climate_news(keyword):
    API_KEY = "a5e893cdb521e63052bf12eeafb0737c"  # Remplace avec ta clé API Mediastack
    url = f"http://api.mediastack.com/v1/news?access_key={API_KEY}&categories=general&keywords={keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        return news_data['data']
    else:
        return None

# CSS pour le style du logo (alignement et taille)
st.markdown("""
    <style>
    .logo-container {
        display: flex;
        align-items: left;
        justify-content: left;
        margin-bottom: 20px;
    }
    .logo-container img {
        width: 150px;  /* Ajuste la taille ici */
        height: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Onglet Accueil avec le logo animé
def display_accueil():
    # Afficher le logo animé à gauche
    st.markdown("""
    <div class="logo-container">
        <img src="C:/Users/patrick/Downloads/Ecotrace_web/logo.gif" alt="EcoTrace Logo">
    </div>
    """, unsafe_allow_html=True)

    # Contenu principal de l'accueil
    st.title("Bienvenue sur EcoTrace")
    st.write("""
        **EcoTrace** est une plateforme numérique innovante qui simplifie la gestion des déchets recyclables  au Cameroun. 
        En facilitant le recyclage et la réduction des déchets, EcoTrace contribue à un environnement plus propre et à une économie verte durable. 
        Les utilisateurs peuvent non seulement signaler leurs déchets, mais aussi suivre leur collecte en temps réel et gagner des récompenses pour leur participation active.
    """)

    # Section Recherche des actualités sur la Justice Climatique
    st.subheader("Recherchez des actualités sur la Justice Climatique")
    
    # Ajout d'une barre de recherche pour les actualités
    keyword = st.text_input("Entrez un mot-clé pour rechercher des actualités", value="climate change")
    
    if keyword:
        st.write(f"Résultats pour : {keyword}")
        news = get_climate_news(keyword)

        if news:
            for article in news[:5]:  # Limiter à 5 articles
                st.markdown(f"**[{article['title']}]({article['url']})**")
                st.write(f"*Source : {article['source']} | Date : {article['published_at']}*")
                st.write(f"{article['description']}")

                # Affichage conditionnel de l'image
                if article.get('image'):
                    st.image(article['image'], use_column_width=True)
                else:
                    st.write("Pas d'image disponible")
                
                st.write("---")
        else:
            st.error("Erreur de chargement des actualités. Veuillez réessayer plus tard.")
    else:
        st.write("Entrez un mot-clé pour afficher les résultats.")

        #________++++++++++++++++++++++++++++++++++++++++++++++______________+++++++++++++++
               
    # Fonction pour envoyer un SMS
# Configuration Twilio
account_sid = 'AC4e99121e3b36cc59ecc10d595dced23e'  # Remplace par ton SID de compte Twilio
auth_token = 'c164df4c76938fd563695177b944b68a'  # Remplace par ton token d'authentification Twilio
twilio_phone_number = '+13346058063'  # Numéro Twilio pour l'envoi de SMS
your_phone_number = '+237673281383'  # Numéro où le SMS sera envoyé
client = Client(account_sid, auth_token)

# Fonction pour envoyer un SMS
def send_sms(body):
    try:
        # Envoie le message à ton propre numéro
        message = client.messages.create(
            body=body,
            from_=twilio_phone_number,
            to=your_phone_number  # Utilise ton propre numéro ici
        )
        return True
    except Exception as e:
        st.error(f"Erreur lors de l'envoi du SMS : {e}")
        return False
    
# Onglet Signaler des Déchets
def display_signal_dechets():
    st.title("Signaler des Déchets")

    # Formulaire de signalement
    with st.form("report_form"):
        type_dechets = st.selectbox("Type de Déchets", ["Plastique", "Verre", "Métal", "Papier", "Autre"])
        quantite = st.number_input("Quantité", min_value=1, placeholder="Entrez la quantité de déchets")
        description = st.text_area("Description", placeholder="Décrivez les déchets signalés et votre numero money")
        adresse = st.text_input("Votre Adresse", placeholder="Entrez votre adresse  ici")
        
        submit_button = st.form_submit_button("Signaler")

        if submit_button:
            # Construire le message à envoyer
            body = f"""
            Type de Déchets: {type_dechets}
            Quantité: {quantite}
            Description: {description}
            Adresse: {adresse}
            """
            if send_sms(body):
                st.success("Votre signalement a été envoyé avec succès !")
            else:
                st.error("Échec de l'envoi du signalement.")
#----------------------------------------------------------###############################################################

# Connexion à la base de données SQLite
def connect_db():
    conn = sqlite3.connect('ecotrace.db')
    return conn

# Fonction pour récupérer les données de collecte depuis SQLite
def get_collecte_data_from_db():
    conn = connect_db()
    query = "SELECT zone, type_dechets, quantite_kg, progres_percent, latitude, longitude, image_url FROM collecte_dechets"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Fonction pour afficher les notifications (par exemple : collecte terminée, retard)
def send_notification(type, zone):
    if type == "retard":
        st.warning(f"La collecte dans la zone {zone} est en retard.")
    elif type == "terminée":
        st.success(f"La collecte dans la zone {zone} est terminée.")

# Fonction pour afficher les données de collecte avec carte et photos
def display_suivi_collecte():
    st.title("Suivi de la Collecte")

    # Charger les données depuis la base de données SQLite
    data = get_collecte_data_from_db()

    # Filtre pour le type de déchets ou la zone
    st.sidebar.subheader("Filtrer les collectes")
    selected_zone = st.sidebar.selectbox("Sélectionner une zone", data["zone"].unique())
    selected_type_dechets = st.sidebar.selectbox("Sélectionner le type de déchets", data["type_dechets"].unique())
    
    # Filtrer les données en fonction des sélections
    filtered_data = data[(data["zone"] == selected_zone) & (data["type_dechets"] == selected_type_dechets)]

    # Notifications Push pour retard ou collecte terminée
    for i, row in filtered_data.iterrows():
        if row['progres_percent'] < 100:
            send_notification("retard", row['zone'])
        else:
            send_notification("terminée", row['zone'])
    
    # Carte interactive pour suivre les camions de collecte
    st.subheader("Carte en Temps Réel des Collectes")
    m = folium.Map(location=[3.8480, 11.502], zoom_start=13)
    
    for i, row in filtered_data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Zone: {row['zone']}<br>Progrès: {row['progres_percent']}%<br>Type de Déchets: {row['type_dechets']}",
            tooltip=row['zone'],
            icon=folium.Icon(color="green" if row["progres_percent"] == 100 else "orange"),
        ).add_to(m)
    
    folium_static(m)
    
    # Graphique interactif des déchets collectés par zone
    st.subheader(f"Graphique des Déchets Collectés pour {selected_zone}")
    fig = px.bar(filtered_data, x="zone", y="quantite_kg", color="progres_percent", 
                 title="Quantité de Déchets Collectés par Zone",
                 labels={"quantite_kg": "Déchets Collectés (kg)"})
    st.plotly_chart(fig)

    # Afficher la progression de la collecte
    st.subheader(f"Progression de la Collecte pour {selected_zone}")
    for i, row in filtered_data.iterrows():
        st.progress(row['progres_percent'])

    # Affichage des photos des zones collectées
    st.subheader(f"Photos des zones collectées ({selected_zone})")
    for i, row in filtered_data.iterrows():
        if row["image_url"]:
            st.image(row["image_url"], caption=f"Photo de {row['zone']}", use_column_width=True)
        else:
            st.info(f"Aucune image disponible pour {row['zone']}.")

        #-------------------------------------------------------3----------------------------------------------

        # Connexion à la base de données SQLite ecotrace.db
conn = sqlite3.connect('ecotrace.db')
cursor = conn.cursor()

# Fonction pour afficher les récompenses d'un utilisateur
def afficher_recompenses(utilisateur):
    # Requête pour récupérer les récompenses depuis la table 'rewards'
    cursor.execute('SELECT * FROM rewards WHERE utilisateur=?', (utilisateur,))
    recompenses = cursor.fetchall()
    
    if recompenses:
        st.subheader(f"🎉 Récompenses pour {utilisateur} 🎉")
        
        # Animation simulée lors de l'affichage des récompenses
        progress_bar = st.progress(0)
        for index, recompense in enumerate(recompenses):
            progress = (index + 1) / len(recompenses)
            time.sleep(0.5)  # Simuler un délai pour l'animation
            progress_bar.progress(int(progress * 100))
            
            st.write(f"🏅 **Récompense ID**: {recompense[0]}")
            st.write(f"⭐ **Points**: {recompense[2]}")
            st.write(f"💵 **Montant (FCFA)**: {recompense[3]}")
            st.write(f"💬 **Description**: {recompense[4]}")
            st.write("———")
        
        progress_bar.empty()  # Supprimer la barre de progression une fois terminé
    else:
        st.write(f"❌ Aucune récompense trouvée pour **{utilisateur}**.")

# Onglet Récompenses
def display_recompenses():
    st.title("🏆 Récompenses")

    # Sélection de l'utilisateur pour voir ses récompenses
    utilisateur = st.text_input("🔍 Entrez votre nom d'utilisateur pour consulter vos récompenses")
    
    if utilisateur:
        afficher_recompenses(utilisateur)
    
    st.subheader("💡 Comment gagner des récompenses ?")
    st.write("""
    - 🗑️ **Signaler des déchets** : Chaque fois que vous signalez des déchets collectés, vous gagnez des points.
    - 🤝 **Participer à des collectes** : Vous pouvez gagner plus de points en participant aux collectes organisées.
    - 🎁 **Récompenses Bonus** : Gagnez des points supplémentaires en signalant des déchets dans des zones spécifiques ou en participant à des événements spéciaux.
    """)


    #______________________________________________________#______________________________________________________________

# Connexion à la base de données SQLite ecotrace.db
conn = sqlite3.connect('ecotrace.db')
cursor = conn.cursor()

# Fonction pour récupérer les données de collecte
def get_collecte_data():
    cursor.execute('SELECT type_dechets, SUM(quantite_kg) as total_kg FROM collecte_dechets GROUP BY type_dechets')
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=['Type de Déchets', 'Total KG'])

def get_volume_total():
    cursor.execute('SELECT SUM(quantite_kg) FROM collecte_dechets')
    return cursor.fetchone()[0] or 0

# Fonction pour afficher les statistiques
def display_statistics():
    st.title("📊 Statistiques et Analyses")

    # Récupérer les données de collecte
    collecte_df = get_collecte_data()
    total_volume = get_volume_total()

    # Disposition des graphiques en trois colonnes
    col1, col2, col3 = st.columns(3)

    if not collecte_df.empty:
        # Graphique à barres - Volume de déchets recyclés par type
        with col1:
            st.subheader("📈 Volume de déchets par type")
            fig1, ax1 = plt.subplots()
            ax1.bar(collecte_df['Type de Déchets'], collecte_df['Total KG'], color='skyblue')
            ax1.set_xlabel("Type de Déchets")
            ax1.set_ylabel("Volume Recyclé (KG)")
            ax1.set_title("Volume de déchets recyclés par type")
            plt.xticks(rotation=45)
            st.pyplot(fig1)

        # Graphique à secteurs - Répartition des déchets par type
        with col2:
            st.subheader("🍰 Répartition des déchets par type")
            fig2, ax2 = plt.subplots()
            ax2.pie(collecte_df['Total KG'], labels=collecte_df['Type de Déchets'], autopct='%1.1f%%', startangle=90)
            ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig2)

        # Graphique linéaire - Volume total de déchets au fil du temps
        # Remplacer avec vos données temporelles si disponibles
        # Ici, on simule des données temporelles
        dates = pd.date_range(start='2023-01-01', periods=len(collecte_df), freq='M')
        simulated_volumes = collecte_df['Total KG'].cumsum()  # Volume cumulatif pour l'exemple

        with col3:
            st.subheader("📊 Volume total de déchets au fil du temps")
            fig3, ax3 = plt.subplots()
            ax3.plot(dates, simulated_volumes, marker='o', color='green')
            ax3.set_xlabel("Date")
            ax3.set_ylabel("Volume Cumulé (KG)")
            ax3.set_title("Volume total de déchets au fil du temps")
            plt.xticks(rotation=45)
            st.pyplot(fig3)

    else:
        st.write("❌ Aucune donnée de collecte disponible.")

        #-------------------------------------------------------#_____________________________________________________

        # Fonction pour envoyer un email
def envoyer_email(nom, email, message):
    try:
        # Configuration de l'email
        msg = MIMEText(f"Nom: {nom}\nEmail: {email}\nMessage: {message}")
        msg['Subject'] = 'Nouveau message de support'
        msg['From'] = 'votre_email@example.com'  # Remplacez par votre adresse email
        msg['To'] = email  # Adresse email de l'utilisateur qui a soumis le formulaire

        # Connexion au serveur SMTP
        with smtplib.SMTP('smtp.example.com', 587) as server:  # Remplacez par votre serveur SMTP
            server.starttls()
            server.login('votre_email@example.com', 'votre_mot_de_passe')  # Authentifiez-vous
            server.send_message(msg)

        return True
    except Exception as e:
        st.error(f"Erreur lors de l'envoi de l'email : {e}")
        return False

# Onglet Contact et Assistance
def display_contact_assistance():
    st.title("📞 Contact et Assistance")

    # Informations de contact
    st.header("Informations de Contact")
    st.write("Pour toute question ou assistance, vous pouvez nous contacter par les moyens suivants :")
    st.write("- **Email :** patcelest237@gmail.com")
    st.write("- **Téléphone :** +237 620 705 361")
    st.write("- **Adresse :** 123 Rue de l'Ecologie, Yaoundé, Cameroun")

    # Section FAQ
    st.header("📚 FAQ")
    st.write("Voici quelques questions fréquemment posées :")
    
    faqs = {
        "Q1: Comment signaler des déchets ?": "Vous pouvez signaler des déchets en utilisant l'onglet 'Signaler des Déchets' de notre application.",
        "Q2: Comment gagner des récompenses ?": "Gagnez des récompenses en signalant des déchets et en participant à nos collectes.",
        "Q3: Quelles sont les zones couvertes par le service ?": "Nous couvrons actuellement plusieurs zones à Yaoundé. Consultez notre carte dans l'onglet 'Suivi de la Collecte'.",
        "Q4: Comment puis-je participer à une collecte ?": "Les annonces de collecte sont publiées sur notre application. Restez à l'affût des notifications !",
        "Q5: Que faire si je rencontre un problème avec l'application ?": "Vous pouvez nous contacter via ce formulaire ou consulter la FAQ pour plus d'informations."
    }

    for question, answer in faqs.items():
        st.write(f"**{question}**")
        st.write(answer)

    # Formulaire de support
    st.header("🆘 Formulaire de Support")
    with st.form("support_form"):
        nom = st.text_input("Votre Nom")
        email = st.text_input("Votre Email")
        message = st.text_area("Votre Message ou Question")
        submit_button = st.form_submit_button("Envoyer")

        if submit_button:
            if envoyer_email(nom, email, message):
                st.success("Votre message a été envoyé avec succès ! Nous vous contacterons bientôt.")

#-----------------------------------#_----------------------------------------------------------------------

# Custom CSS

st.markdown("""
    <style>
    body {
        font-family: 'Helvetica', sans-serif;
        color: #2E7D32;
    }
    .stButton>button {
        background-color: #2E7D32;
        color: white;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        color: white;
    }
    h1 {
        color: #1B5E20;
    }
    h2 {
        color: #388E3C;
    }
    </style>
    """, unsafe_allow_html=True)





# Onglets principaux
tabs = ["Accueil", "Signaler des Déchets", "Suivi de la Collecte", "Récompenses", "Statistiques et Analyses", "Contact et Assistance"]
page = st.sidebar.selectbox("Navigation", tabs)

# Accueil
if page == "Accueil":
     display_accueil()
    

# Signaler des Déchets
elif page == "Signaler des Déchets":
    display_signal_dechets()
    
   

# Suivi de la Collecte
elif page == "Suivi de la Collecte":
    st.header("Suivi en temps réel des collectes")
    st.write("Bientôt disponible : Suivez vos collectes ici en temps réel.")
    display_suivi_collecte()

# Récompenses
elif page == "Récompenses":
    st.header("Récompenses")
    st.write("Accumulez des points pour chaque signalement et transformez-les en récompenses monétaires ou en bons d'achat.")

     # Afficher l'onglet Récompenses
    display_recompenses()




# Statistiques et Analyses
elif page == "Statistiques et Analyses":
   
    # Placeholder pour les graphiques futurs
    display_statistics()

# Contact et Assistance
elif page == "Contact et Assistance":
      display_contact_assistance()
