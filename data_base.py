import sqlite3 as sq
from contextlib import closing

from reader import Reader as r

DB_PATH = 'coocurence_data_base.db'
CONNECTION_ARGS = 'file:{}?mode={}'

GET_VOCABULARY = 'SELECT id, word FROM vocabulary_table;'
GET_WORD_INDEX = 'SELECT id FROM vocabulary_table WHERE word = (?);'
GET_INDEX_WORD = 'SELECT word FROM vocabulary_table WHERE id = (?);'
GET_COOCURENCE = 'SELECT * FROM (?) WHERE id_word = (?) AND id_adjacent_word = (?)'
GET_COOCURENCE_TABLE = 'SELECT * FROM {} '
GET_STOP_LIST = 'SELECT word FROM stop_word_table'

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


INSERT_NEW_WORD = 'INSERT OR IGNORE INTO vocabulary_table (id, word) VALUES (?, ?); '
INSERT_FIRST_WORD = 'INSERT INTO vocabulary_table (id ,word) VALUES (0, ?); '
INSERT_NEW_OCCURENCE = 'INSERT OR IGNORE INTO (?) VALUES ( ?, ? , ? ) IF NOT EXISTS;'
INSERT_STOP_LIST = 'INSERT INTO stop_word_table (word) VALUES( ? );'

UPDATE_COOCCURENCE = 'INSERT or REPLACE INTO {}(id_word, id_adjacent_word, occurences) VALUES( ? , ? , ? );'

COUNT_VOCABULARY = 'SELECT COUNT(*) FROM vocabulary_table'


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

    def get_vocabulary(self):
        with closing(self.connection.cursor()) as c:
            c.execute(GET_VOCABULARY)
            list_word = [x[1] for x in c.fetchall()]
            return list_word

    def get_coocurence_table(self, table_name):
        try:
            get_coocurence_table = GET_COOCURENCE_TABLE.format(table_name)
            with closing(self.connection.cursor()) as c:
                c.execute(get_coocurence_table)
                result = c.fetchall()
                result = {(row[0], row[1]): row[2] for row in result}
                return result
        except sq.OperationalError:
            return

    def get_connection(self):
        connection_string = CONNECTION_ARGS.format(DB_PATH, 'rw')
        connexion = sq.connect(connection_string, uri=True)
        return connexion

    def get_vocabulary_length(self):
        with closing(self.connection.cursor()) as c:
            c.execute(COUNT_VOCABULARY)
            return c.fetchone()[0]

    def get_stop_list(self):
        with closing(self.connection.cursor()) as c:
            c.execute(GET_STOP_LIST)
            result = c.fetchall()
            return [word[0] for word in result]

    def add_stop_word(self, stopworditer):
        with closing(self.connection.cursor()) as c:
            c.executemany(INSERT_STOP_LIST, stopworditer)

    def add_words(self, worditer):
        with closing(self.connection.cursor()) as c:
            c.executemany(INSERT_NEW_WORD, worditer)

    def update_coocurence(self, table_name, coocurence_iter):
        update_querry = UPDATE_COOCCURENCE.format(table_name)
        with closing(self.connection.cursor()) as c:
            c.executemany(update_querry, coocurence_iter)

    def commit(self):
        self.connection.commit()
        print('commit')

    def create_coocurence_table(self, table_name):
        with closing(self.connection.cursor()) as c:
            c.execute(CREATE_COOCURENCE_TABLE.format(table_name))
            try:
                c.execute(CREATE_COMPOSITE_INDEX.format(table_name, table_name))
            except sq.OperationalError:
                pass

    def create_database(self):
        connection_string = CONNECTION_ARGS.format(DB_PATH, 'rwc')
        connection = sq.connect(connection_string, uri=True, isolation_level='DEFERRED')
        with closing(connection.cursor()) as c:
            c.execute('''PRAGMA synchronous = OFF''')
            c.execute('''PRAGMA journal_mode = OFF''')
            c.execute(CREATE_INDEXES_TABLE)
            c.execute(CREATE_UNIQUE_INDEX.format('vocabulary_index', 'vocabulary_table'))
            c.execute(CREATE_STOP_LIST)
            c.execute(CREATE_UNIQUE_INDEX.format('stop_word_index', 'stop_word_table'))
            c.executemany(INSERT_STOP_LIST, r.read_stoplist())
        connection.commit()
        return connection
