from numpy.core.defchararray import lower
import re
import data_base as db

class Reader:
    @staticmethod
    def read(encoding, paths):
        full_text = str()
        for path in paths:
            with open(path, 'r', encoding=encoding) as text:
                full_text += text.read()
            text.close()
        return full_text

    @staticmethod
    def read_stoplist():
            stoplist = Reader.read('utf-8', ['stopword.txt'])
            stoplist = stoplist.splitlines()
            for line in stoplist:
                db.Data_Base.add_stop_word(line)

            db.Data_Base.get_connection(db.DB_PATH).commit()


    @staticmethod
    def read_text(encoding, paths):
        full_text = Reader.read(encoding, paths)
        full_text = lower(re.findall('(\w+|[!?])', full_text))
        return full_text