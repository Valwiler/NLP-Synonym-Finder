import sqlite3 as sq

GET_WORD_INDEX = '/SELECT ind FROM (?) WHERE word = (?)'

CREATE_INDEXES_TABLE = ' CREATE TABLE vocabulary_table IF NOT EXISTS (' \
                       'id INT NOT NULL AUTO INCREMENT ,' \
                       'word char(50) NOT NULL,' \
                       'PRIMARY KEY (id)' \
                       'CREATE UNIQUE INDEX vocabulary_index ON word )'

CREATE_COOCURENCE_TABLE = ' CREATE TABLE (?) IF NOT EXISTS  (' \
                          'id_word INT NOT NULL, ' \
                          'id_adjacent_word INT NOT NULL,' \
                          'occurences INT NOT NULL,' \
                          'FOREIGN KEY (id_word) REFERENCES vocabulary_table(id),' \
                          'FOREIGN KEY (id_adjacent_word) REFERENCES vocabulary_table(id))'

INSERT_NEW_WORD = 'INSERT INTO vocabulary_table VALUES( ? ) IF NOT EXISTS'
INSERT_NEW_OCCURENCE = 'INSERT INTO (?) VALUES ( ?, ? , ? ) IF NOT EXISTS'  # toujouts penser a initialiser le nombre d'occurence a 0
UPDATE_OCCURENCE = 'UPDATE (?) SET occurences = +1 WHERE id_word = (?) AND id_adjacent_word = (?)'


class Data_Base:
    def __init__(self):
        DB_PATH = 'coocurence_data_base.db'
        self.connexion = sq.connect(DB_PATH)
        self.cursor = self.connexion.cursor()
        self.cursor.execute('PRAGMA foreign_keys = 1')

    def get_word_index(self):
        pass
        # retourne l'idex du mot

    def add_word(self):
        pass
        # ajoute le mot
