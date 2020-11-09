import sqlite3 as sq


class Data_Base:
    def __init__(self):
        DB_PATH = 'coocurence_data_base.db'
        self.connexion = sq.connect(DB_PATH)
        self.cursor = self.connexion.cursor()
        self.cursor.execute('PRAGMA foreign_keys = 1')
