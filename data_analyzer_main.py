import os

from trainer import Trainer as tr
from finder import Finder as f
from reader import writer as wr
import pathlib


class Data_Analyzer:

    # def __init__(self, maximal_window_size, maximal_cluster_number, paths, encoding, report_path, result_per_cluster):
    def __init__(self, window_size, cluster_number, paths, encoding, report_path, result_per_cluster):
        self.train_all_windows(paths, encoding, window_size)

        # self.run_clustering_finder(maximal_window_size, maximal_cluster_number, report_path, result_per_cluster)
        self.run_clustering_mono_cluster_number(window_size, cluster_number, result_per_cluster, report_path)

    def train_all_windows(self, paths, encoding, maximal_window_size):
        # for i in range(2, maximal_window_size, 2):
        #     trainer = tr(i)
        #     print(os.listdir())
        #     print(paths)
            trainer = tr(maximal_window_size)
            trainer.process_text(encoding, paths)
    #
    # def run_clustering_finder(self, maximal_window_size, maximal_cluster_number, report_path, result_per_cluster):
    #     for window_size in range(2, maximal_window_size, 2):
    #         print("Window size iter:" + str(window_size) + " of " + str(maximal_window_size))
    #         finder = f(window_size)
    #         print("still running: new window size")
    #         for cluster_number in range(1, maximal_cluster_number):
    #             print("cluster number iter:" + str(cluster_number) + " of " + str(maximal_cluster_number))
    #             print("still running: new cluster number")
    #             clusters, targets = finder.generate_random_clusters(cluster_number, result_per_cluster)
    #
    #             wr.save_cluster_report("wn" + str(window_size) + "cn" + str(cluster_number) + report_path,
    #                                    targets, clusters, window_size)
    #             print("report updated at " + "wn" + str(window_size) + "cn" + str(cluster_number) + report_path + "!")

    def run_clustering_mono_cluster_number(self, window_size, cluster_number, result_per_cluster, report_path):

        print("Window size iter:" + str(window_size))
        finder = f(window_size)
        clusters, targets = finder.generate_random_clusters(cluster_number, result_per_cluster)

        wr.save_cluster_report("wn" + str(window_size) + "cn" + str(cluster_number) + report_path,
                               targets, clusters, window_size)
        print("report updated at " + "wn" + str(window_size) + "cn" + str(cluster_number) + report_path + "!")


if __name__ == '__main__':
    path = pathlib.Path(r'C:\Users\Tom\Desktop\b52-tp2\textes\LesTroisMousquetairesUTF8.txt')
    # path.
    test = Data_Analyzer(10,
                         10,
                         ['textes\\LesTroisMousquetairesUTF8.txt', 'textes\\GerminalUTF8.txt', 'textes\\LeVentreDeParisUTF8.txt'],
                         'UTF-8',
                         'test.csv',
                         10)
