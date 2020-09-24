import numpy as np
import re


class Reader:
    def __init__(self, widow_size, encoding, paths):
        self.widow_size = int(widow_size/2)
        self.encoding = encoding
        self.paths = paths
        self.word_index = dict()
        self.text_list = list()
        self.read()
        self.index()
        self.result_array = self.match()
        print(self.result_array)

    def read(self):
        for path in self.paths:
            f = open(path, 'r', encoding=self.encoding)
            self.text_list.append(f.read())

    def index(self):
        current_index = 0
        for text in self.text_list:
            for word in filter(None, re.split('[\-.,\'\";:«»!?\s]', text)):
                if word not in self.word_index.keys():
                    self.word_index[word] = current_index
                    current_index += 1
        print(self.word_index)

    def match(self):
        result_array = np.zeros((len(self.word_index), len(self.word_index)))
        for text in self.text_list:
            for word in self.word_index.keys():
                regex = '((?:[a-zA-ZÀ-ÿ]*[.!?,\'\";:\s]*){' + str(self.widow_size) + \
                        '})[.!?,\'\";:\s]*' + word +'[.!?,\'\";:\s]*((?:[a-zA-ZÀ-ÿ]*[.!?,\'\";:\s]*){'+\
                        str(self.widow_size) +'})'
                match_result = re.findall(regex,text)
                if match_result:
                    for result in match_result:
                        for result_group in result:
                            for result_word in filter(None, re.split('[\-.,\'\";:«»!?\s]', result_group)):
                                result_array[self.word_index.get(word)][self.word_index.get(result_word)] += 1
        return result_array




if __name__ == '__main__':
    Reader(5, 'utf-8', ['test.txt'])
