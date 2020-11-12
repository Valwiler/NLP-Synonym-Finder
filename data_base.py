import sqlite3 as sq
from contextlib import closing
from reader import Reader as r

GET_VOCABULARY = 'SELECT id, word FROM vocabulary_table;'
GET_WORD_INDEX = 'SELECT id FROM vocabulary_table WHERE word = (?);'
GET_INDEX_WORD = 'SELECT word FROM vocabulary_table WHERE id = (?);'
GET_COOCURENCE = 'SELECT * FROM (?) WHERE id_word = (?) AND id_adjacent_word = (?)'
GET_COOCURENCE_TABLE = 'SELECT * FROM {} '

DB_PATH = 'coocurence_data_base.db'
CONNECTION_ARGS = 'file:{}?mode={}'

CREATE_INDEXES_TABLE = 'CREATE TABLE IF NOT EXISTS vocabulary_table  (' \
                       'id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                       'word TEXT NOT NULL);'

CREATE_UNIQUE_INDEX = 'CREATE UNIQUE INDEX {} ON {}(word);'
CREATE_COMPOSITE_INDEX = 'CREATE UNIQUE INDEX cooc_index_{} ON {}(id_word, id_adjacent_word);'

CREATE_COOCURENCE_TABLE = '''CREATE TABLE IF NOT EXISTS {}
                          (
                          id_word INTEGER  NOT NULL,
                          id_adjacent_word INTEGER NOT NULL,
                          occurences INTEGER NOT NULL,
                          FOREIGN KEY (id_word) REFERENCES vocabulary_table(id),
                          FOREIGN KEY (id_adjacent_word) REFERENCES vocabulary_table(id)
                          );'''

CREATE_STOP_LIST = 'CREATE TABLE IF NOT EXISTS stop_word_table (' \
                   'word TEXT NOT NULL);'

INSERT_NEW_WORD = 'INSERT OR IGNORE INTO vocabulary_table (word) VALUES (?); '
INSERT_NEW_OCCURENCE = 'INSERT OR IGNORE INTO (?) VALUES ( ?, ? , ? ) IF NOT EXISTS;'

UPDATE_OCCURENCE = 'UPDATE (?) OR IGNORE SET SUM(occurences , (?)) WHERE id_word = (?) AND id_adjacent_word = (?);'

# UPSERT_OCCURENCE = '''INSERT INTO cooc_size2(id_word, id_adjacent_word, occurences) VALUES (?,?,?)
#                       ON CONFLICT (id_word) WHERE id_word = (?) AND id_adjacent_word = (?)
#                       DO UPDATE SET  occurences = occurences + (?)'''

# WHERE id_word = (?) AND id_adjacent_word = (?);
INSERT_STOP_LIST = 'INSERT INTO stop_word_table (word) VALUES( ? );'

SELECT_COOCURENCE = 'SELECT * FROM {} WHERE id_word = (?) AND id_adjacent_word = (?)'


class Data_Base:
    __instance = None

    @staticmethod
    def getInstance():
        if Data_Base.__instance is None:
            Data_Base()
        return Data_Base.__instance

    def __init__(self):
        try:
            self.connection = self.get_connection()
        except sq.OperationalError:
            self.connection = self.create_database()
        Data_Base.__instance = self

    # BROKEN
    def get_word_index(self, word):
        with closing(self.connection.cursor()) as c:
            c.execute(GET_WORD_INDEX, (word,))
            return c.fetchall()

    def get_index_word(self, index):
        with closing(self.connection.cursor()) as c:
            c.execute(GET_INDEX_WORD, (index,))
            return c.fetchall()

    def get_vocabulary(self):
        with closing(self.connection.cursor()) as c:
            c.execute(GET_VOCABULARY)
            return c.fetchall()

    def get_coocurence_table(self, table_name):
        get_coocurence_table = GET_COOCURENCE_TABLE.format(table_name)
        with closing(self.connection.cursor()) as c:
            c.execute(get_coocurence_table)
            result = c.fetchall()
            result = {(row[0], row[1]): row[2] for row in result}
            return result

    def add_stop_word(self, stopworditer):
        with closing(self.connection.cursor()) as c:
            c.executemany(INSERT_STOP_LIST, stopworditer)

    def add_words(self, worditer):
        with closing(self.connection.cursor()) as c:
            c.executemany(INSERT_NEW_WORD, worditer)

    # def upsert_coocurence(self, table_name, coocurence_iter):
    #     upsert_querry = UPSERT_OCCURENCE.format(table_name)
    #     with closing(self.connection.cursor()) as c:
    #         c.executemany(upsert_querry, coocurence_iter)
    #
    # def select_coocurence(self, table_name, ids):
    #     select_querry = SELECT_COOCURENCE.format(table_name)
    #     with closing(self.connection.cursor()) as c:
    #         c.execute(select_querry, (ids[0], ids[1],))
    #         return c.fetchall()

    def commit(self):
        self.connection.commit()
        print('commit')

    def get_connection(self):
        connection_string = CONNECTION_ARGS.format(DB_PATH, 'rw')
        connexion = sq.connect(connection_string, uri=True)
        return connexion

    def create_coocurence_table(self, table_name):
        with closing(self.connection.cursor()) as c:
            c.execute(CREATE_COOCURENCE_TABLE.format(table_name))
            try:
                c.execute(CREATE_COMPOSITE_INDEX.format(table_name, table_name))
            except sq.OperationalError:
                pass

    # def get_cursor(self):
    #     return self.connection.cursor()

    def create_database(self):
        connection_string = CONNECTION_ARGS.format(DB_PATH, 'rwc')
        connexion = sq.connect(connection_string, uri=True, isolation_level='DEFERRED')
        with closing(connexion.cursor()) as c:
            c.execute('''PRAGMA synchronous = OFF''')
            c.execute('''PRAGMA journal_mode = OFF''')
            c.execute(CREATE_INDEXES_TABLE)
            c.execute(CREATE_UNIQUE_INDEX.format('vocabulary_index', 'vocabulary_table'))
            c.execute(CREATE_STOP_LIST)
            c.execute(CREATE_UNIQUE_INDEX.format('stop_word_index', 'stop_word_table'))
            c.executemany(INSERT_STOP_LIST, r.read_stoplist())
        connexion.commit()
        return connexion


if __name__ == '__main__':
    Data_Base.getInstance()
