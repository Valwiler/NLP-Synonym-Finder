from numpy.core.defchararray import lower
import chrono as ch
import re


class Reader:
    @staticmethod
    def read(encoding, paths):
        full_text = str()
        for path in paths:
            with open(path, 'r', encoding=encoding) as text:
                full_text += text.read()
            text.close()
        full_text = lower(re.findall('(\w+|[!?])', full_text))
        return full_text
