import argv_parser as arg
from trainer import Trainer as tr
from finder import Finder as sf
from experiment import Experiment as exp


def main():
    arguments = arg.ArgvParser
    paths = arguments.getInstance().filesPath()
    window = arguments.getInstance().windowSize()
    encoding = arguments.getInstance().encoding()

    if arguments.getInstance().isTrainingMode():
        trainer = tr(window)
        trainer.process_text(encoding, paths)
    elif arguments.getInstance().isResearchMode():
        synonym_finder = sf(window)
        while True:
            buffer = input('\nEntrez un mot, le nombre de synonymes que vous voulez et la methode de calcul.\n'
                           '( i.e. produit scalaire: 0, least-squares:1, city-block:2 )\n\n'
                           '\t\t\t\t\t\t\t Tapez q pour quitter.\n\n\t')
            try:
                if buffer == 'q':
                    quit()
                else:
                    target_word, result_number, training_method = buffer.split()
                if int(training_method) > 2:
                    raise ValueError('Methode invalide')
                results = synonym_finder.find_synonym(target_word, int(result_number), int(training_method))
                print('\n')
                for result in results:
                    print(result[0] + ' --> ' + str(result[1]))
                print('\n')
            except ValueError as e:
                print('\n' + str(e))
                continue
    elif arguments.getInstance().isClusteringMode():
        print("Starting experiment with provided parameter")
        exp(window,arguments.getInstance().clusterNumber(), encoding, arguments.getInstance().resultNumber())




if __name__ == '__main__':
    main()
