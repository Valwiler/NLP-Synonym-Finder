import sys
import trainer as t
import argv_parser as arg
import data_base as db


# Loop principale du programme

def main():
    arguments = arg.ArgvParser
    paths = arguments.filesPath(arguments.getInstance())
    window = arguments.windowSize(arguments.getInstance())
    encoding = arguments.encoding(arguments.getInstance())
    DB = db.Data_Base()

    while True:
        buffer = input('\nEntrez un mot, le nombre de synonymes que vous voulez et la methode de calcul.\n'
                       '( i.e. produit scalaire: 0, least-squares:1, city-block:2 )\n\n'
                       '\t\t\t\t\t\t\t Tapez q pour quitter.\n\n\t')
        try:
            if buffer == 'q':
                quit()
            else:
                target_word, result_nb, method = buffer.split()
            if int(method) > 2:
                raise ValueError('Methode invalide')
            trainer = t.Trainer(target_word, int(result_nb), window, encoding, paths)
            results = trainer.training(int(method))
            print('\n')
            for result in results:
                print(result[0] + ' --> ' + str(result[1]))
            print('\n')
        except ValueError as e:
            print('\n' + str(e))
            print(str(e.with_traceback()))
            continue


if __name__ == '__main__':
    main()
