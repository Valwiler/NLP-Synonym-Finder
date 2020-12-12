from numpy.core.defchararray import lower
import re
import csv
from clustering import Clustering

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
            yield (line,)

    @staticmethod
    def read_text(encoding, paths):
        print(paths)
        full_text = Reader.read(encoding, paths)
        full_text = lower(re.findall('(\w+|[!?])', full_text))
        return full_text

class writer:
    @staticmethod
    def save_cluster_report(path, clustering):
        with open(path, mode='w') as report_file:
            report_writer = csv.writer(report_file, delimiter=',', quotechar='"')
            report_writer.writerow("Runtime:", clustering.last_runtime)
            report_writer.writerow("Iterations:", clustering.last_nbIteration)
            for i, cluster in enumerate(clustering.clusters):
                report_writer.writerow("Cluster" + i, cluster)