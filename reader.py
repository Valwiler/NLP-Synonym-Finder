from numpy.core.defchararray import lower
import chrono as ch
import re


class Reader:
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
