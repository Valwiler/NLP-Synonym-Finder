import os
from trainer import Trainer as tr
from finder import Finder as f


class Experiment:
    def __init__(self, window_size, cluster_number,encoding, result_per_cluster, paths=["textes/GerminalUTF8.txt", "textes/LesTroisMousquetairesUTF8.txt", "textes/LeVentreDeParisUTF8.txt"]):
        self.train_window(window_size,paths, encoding)
        test = self.run_clustering(window_size, cluster_number, result_per_cluster)
        self.write_report(test,window_size,cluster_number, result_per_cluster)


    def run_clustering(self, window_size, cluster_number, result_per_cluster):
        print("Starting clustering for " +str(cluster_number) +  " clusters...")
        finder = f(window_size)
        clusters = finder.generate_random_clusters(cluster_number, result_per_cluster)
        print("Clustering finished!")
        return clusters

    def train_window(self, window_size, paths, encoding):
        print("Processing texts to window size " + str(window_size) + "...")
        trainer = tr(window_size)
        trainer.process_text(encoding, paths)
        print("Processing finished!")

    def write_report(self, clustering, window_size, cluster_number, result_per_cluster):
        with open("reports/res3textes_t" + str(window_size) +
                  "k" + str(cluster_number) +
                  "n" + str(result_per_cluster) + ".txt", mode='w+') as report_file:
            for i, iteration in enumerate(clustering.iterations_stats):
                report_file.write("Itération " + str(i) + "\n")
                report_file.write(str(iteration[1]) + " changements en " + str(iteration[0]) + "secondes\n\n")
                for i,cluste_size in enumerate(iteration[2]):
                    report_file.write("Il y a " + str(cluste_size) + " points (mots) regroupés autour du centroïde no " + str(i) + "\n")
                report_file.write("\n----------------------------------------------------------\n")
            print("Resultats:")
            for i, cluster in enumerate(clustering.clusters):
                report_file.write("Cluster " + str(i) + "\n")
                for result in cluster.points:
                    report_file.write(result[0].identity + " ----> " + str(result[1]) + "\n")
                report_file.write("\n----------------------------------------------------------\n")
            report_file.write("Clustering en " + str(clustering.nbIteration) +
                              " itérations. Temps écoulé:" + str(clustering.runtime) + " secondes.")

if __name__ == '__main__':
    Experiment(5, 4,
               "UTF-8", 10)