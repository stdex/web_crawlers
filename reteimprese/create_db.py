import sqlite3
import os.path
import sys

DATABASE = os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'proxy.db')

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE Reteimprese (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        NOME TEXT,
        INDIRIZZO TEXT,
        CAP TEXT,
        COMUNE TEXT,
        PROVINCIA TEXT,
        TELEONO TEXT,
        PIVA TEXT,
        REA TEXT,
        URL TEXT,
        CATEGORIA TEXT,
        GEOCATEGORIA TEXT,
        URL_RETE_IMPRESA TEXT,
        URL_SEARCH TEXT,
        DESCRIZIONE TEXT,
        IMAGE_URL TEXT,
        SITE_ID TEXT
    )
''')

connection.commit()
connection.close()