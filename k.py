import sqlite3

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('ecotrace.db')
cursor = conn.cursor()

# Création de la table
cursor.execute('''
CREATE TABLE IF NOT EXISTS signalements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    waste_type TEXT,
    quantity INTEGER,
    date_signalement TEXT
)
''')

conn.commit()
conn.close()
