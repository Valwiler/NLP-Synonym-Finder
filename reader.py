from numpy.core.defchararray import lower
import re


class Reader:
    def __init__(self, encoding, paths):
        self.full_text = str()
        self.encoding = encoding
        self.paths = paths

    def read(self):
        for path in self.paths:
            with open(path, 'r', encoding=self.encoding) as book:
                self.full_text += book.read()
        self.full_text = lower(re.findall('(\w+|[!?])', self.full_text))
