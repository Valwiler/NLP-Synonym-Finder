from numpy.core.defchararray import lower
import re


class Reader:
    def __init__(self, encoding, paths):
        self.full_text = str()
        self.encoding = encoding
        self.paths = paths

    def read(self):

        #self.chrono.start()
        for path in self.paths:
            f = open(path, 'r', encoding=self.encoding)
            self.full_text += f.read()
        self.full_text = lower(re.findall('(\w+|[!?])', self.full_text))
        #self.chrono.end()
        #self.chrono.log("read time : ")
