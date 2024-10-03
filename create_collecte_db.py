import sqlite3

# Connexion à la base de données SQLite (ou création si elle n'existe pas)
conn = sqlite3.connect('ecotrace.db')
cursor = conn.cursor()

# Création de la table collecte_dechets
cursor.execute('''
CREATE TABLE IF NOT EXISTS collecte_dechets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone TEXT,
    type_dechets TEXT,
    quantite_kg REAL,
    progres_percent INTEGER,
    latitude REAL,
    longitude REAL,
    image_url TEXT
)
''')

# Création de la table rewards (récompenses)
cursor.execute('''
CREATE TABLE IF NOT EXISTS rewards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur TEXT,
    points INTEGER,
    description TEXT,
    montant_fcfa REAL
)
''')

# Insérer des enregistrements dans la table collecte_dechets avec des liens réels
collecte_data = [
    ("Zone A", "Plastique", 150.5, 75, 3.848, 11.502, "https://www.unep.org/sites/default/files/styles/article_teaser_image/public/2021-10/plastic_pollution.jpg"),
    ("Zone B", "Verre", 200.0, 50, 3.850, 11.505, "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Glass_Recycling.jpg/640px-Glass_Recycling.jpg"),
    ("Zone C", "Métal", 100.0, 90, 3.852, 11.508, "https://upload.wikimedia.org/wikipedia/commons/2/20/Metal_recycling.jpg"),
    ("Zone D", "Papier", 80.0, 100, 3.855, 11.510, "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Paper_recycling_process.jpg/640px-Paper_recycling_process.jpg"),
    ("Zone E", "Plastique", 120.0, 40, 3.860, 11.515, "https://www.unep.org/sites/default/files/styles/full_width_image/public/2021-10/plastic-waste.jpg"),
    ("Zone F", "Verre", 90.5, 60, 3.865, 11.520, "https://upload.wikimedia.org/wikipedia/commons/6/6b/Glass_recycling_1.jpg"),
    ("Zone G", "Métal", 50.0, 20, 3.870, 11.525, "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Metal_scrap_pile.jpg/640px-Metal_scrap_pile.jpg")
]

# Exécution de l'insertion des données de collecte
cursor.executemany('''
    INSERT INTO collecte_dechets (zone, type_dechets, quantite_kg, progres_percent, latitude, longitude, image_url)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', collecte_data)

# Insérer des enregistrements dans la table rewards avec des noms Camerounais et des montants en FCFA
rewards_data = [
    ("Emmanuel Fokou", 120, "Récompense pour signalement de déchets plastiques", 5000),
    ("Marie Tchameni", 150, "Récompense pour collecte de verre", 7000),
    ("Roger Abessolo", 200, "Récompense pour participation à la collecte de métal", 10000),
    ("Esther Nkoum", 180, "Récompense spéciale pour papier", 8500),
    ("Jean-Pierre Ngono", 90, "Récompense pour signalement de déchets organiques", 3000),
    ("Valerie Ntsama", 130, "Récompense pour signalement de déchets plastiques", 5500),
    ("Benoit Ebogo", 170, "Récompense pour participation à la collecte de verre", 9500),
    ("Chantal Mengue", 220, "Récompense pour collecte de métal", 11000),
    ("Cyrille Mvondo", 240, "Récompense pour signalement dans une zone à forte densité", 12500),
    ("Joëlle Kotto", 160, "Récompense pour signalement de plastique et métal", 8000),
    ("Pauline Titi", 140, "Récompense pour signalement de déchets divers", 6000),
    ("Armand Djoumessi", 210, "Récompense pour collecte de papier", 10500),
    ("Lionel Owona", 190, "Récompense pour participation dans plusieurs zones", 9500),
    ("Nathalie Ayissi", 100, "Récompense pour signalement de verre", 4500),
    ("Christian Tchatchoua", 180, "Récompense pour collecte de métal", 8500),
    ("Veronique Ateba", 170, "Récompense pour participation à une campagne de sensibilisation", 9000),
    ("Fabrice Mekoulou", 160, "Récompense pour collecte de plastique", 7500),
    ("Mireille Effa", 140, "Récompense pour signalement de déchets organiques", 6000),
    ("Josephine Mbarga", 130, "Récompense pour participation à une collecte de verre", 5500),
    ("Alain Mveng", 150, "Récompense pour signalement de déchets dans une zone prioritaire", 7000)
]

# Exécution de l'insertion des données de récompenses
cursor.executemany('''
    INSERT INTO rewards (utilisateur, points, description, montant_fcfa)
    VALUES (?, ?, ?, ?)
''', rewards_data)

# Sauvegarde des changements et fermeture de la connexion
conn.commit()
conn.close()

print("La base de données ecotrace.db a été créée avec 7 enregistrements de collecte de déchets et 20 enregistrements de récompenses.")
