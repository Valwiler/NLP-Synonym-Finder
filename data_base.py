import sqlite3 as sq
import os

GET_WORD_INDEX = '/SELECT ind FROM (?) WHERE word = (?)'
DB_PATH = 'coocurence_data_base.db'
CONNECTION_ARGS = 'file:{}?mode={}'

CREATE_INDEXES_TABLE = 'CREATE TABLE IF NOT EXISTS vocabulary_table  (' \
                       'id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                       'word TEXT NOT NULL);'

CREATE_INDEX_ON_INDEXES = 'CREATE UNIQUE INDEX vocabulary_index ON vocabulary_table(word);'

CREATE_COOCURENCE_TABLE = ' CREATE TABLE IF NOT EXISTS c{} (' \
                          'id_word INTEGER  NOT NULL, ' \
                          'id_adjacent_word INTEGER NOT NULL,' \
                          'occurences INTEGER NOT NULL,' \
                          'FOREIGN KEY (id_word) REFERENCES vocabulary_table(id),' \
                          'FOREIGN KEY (id_adjacent_word) REFERENCES vocabulary_table(id));'

CREATE_STOP_LIST = 'CREATE TABLE IF NOT EXISTS stop_word_table ('\
                   'id INTEGER NOT NULL ,  '\
                   'stop_word TEXT NOT NULL, '\
                   'FOREIGN KEY (id) REFERENCES vocabulary_table(id));'

INSERT_NEW_WORD = 'INSERT INTO vocabulary_table VALUES( ? ) IF NOT EXISTS'
INSERT_NEW_OCCURENCE = 'INSERT INTO (?) VALUES ( ?, ? , ? ) IF NOT EXISTS'  # toujouts penser a initialiser le nombre d'occurence a 0
UPDATE_OCCURENCE = 'UPDATE (?) SET occurences = +1 WHERE id_word = (?) AND id_adjacent_word = (?)'

INSERT_STOP_LIST = 'INSERT INTO stop_word_table VALUES( ? ) IF NOT EXISTS '


class Data_Base:
    __instance = None

    @staticmethod
    def getInstance():
        if Data_Base.__instance is None:
            Data_Base()
        return Data_Base.__instance

    def __init__(self):
        try:
            self.connection = self.get_connection(DB_PATH)
        except sq.OperationalError:
            self.connection = self.create_database(DB_PATH)
        Data_Base.__instance = self

    def get_word_index(self, word, table):
        self.cursor.execute(GET_WORD_INDEX, (table, word))
        return self.cursor.fetchall()


    def add_word(self, word):
        self.cursor.execute(INSERT_NEW_WORD, word)

    def get_connection(self, path):
        connection_string = CONNECTION_ARGS.format(path, 'rw')
        connexion = sq.connect(connection_string, uri=True)
        return connexion


    def create_database(self, path):
        connection_string = CONNECTION_ARGS.format(path, 'rwc')
        connexion = sq.connect(connection_string, uri=True)
        c = connexion.cursor()
        c.execute(CREATE_INDEXES_TABLE)
        c.execute(CREATE_INDEX_ON_INDEXES)
        c.execute(CREATE_COOCURENCE_TABLE.format('5'))
        c.execute(CREATE_STOP_LIST)
        connexion.commit()
        return connexion


if __name__ == '__main__':
    Data_Base.getInstance()