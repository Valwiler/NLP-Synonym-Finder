from numpy.core.defchararray import lower
import re


class Reader:
    # Méthode utilisé pour la lecture des différents fichier du corpus et
    # de la stoplist

    @staticmethod
    def read(encoding, paths, **kwargs):
        full_text = str()
        for path in paths:
            with open(path, 'r', encoding=encoding) as text:
                full_text += text.read()
            text.close()
        if 'stoplist' in kwargs:
            full_text = full_text.splitlines()
        else:
            full_text = lower(re.findall('(\w+|[!?])', full_text))
        return full_text
