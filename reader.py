from numpy.core.defchararray import lower
import re
import csv
from pathlib import Path

class Reader:
    @staticmethod
    def read(encoding, paths):
        full_text = str()
        for path in paths:
            path = Path(path)
            with path.open(mode='r', encoding=encoding) as text:
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
        full_text = Reader.read(encoding, paths)
        full_text = lower(re.findall('(\w+|[!?])', full_text))
        return full_text

class writer:
    @staticmethod
    def save_cluster_report(path, mots, clustering, window_size):
        with open(path, mode='w+') as report_file:
            report_writer = csv.writer(report_file, delimiter=',', quotechar='"')
            report_writer.writerow(["Window size:", window_size])
            report_writer.writerow(["Runtime:", clustering.last_runtime])
            report_writer.writerow(["Iterations:", clustering.last_nbIteration])
            report_writer.writerow(["Number of clusters:", len(mots)])
            report_writer.writerow(["Original vectors:"])
            for i, mot in enumerate(mots):
                report_writer.writerow(["Vector" + str(i) ,mot])
            for i, cluster in enumerate(clustering.clusters):
                report_writer.writerow(["Cluster" + str(i)])
                for mot in cluster.points:
                    report_writer.writerow([mot[0].identity, str(mot[1])])