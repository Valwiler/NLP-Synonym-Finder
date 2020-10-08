import sys
import trainer as t

# Loop principale du programme

def main():
    paths = []
    window = int(sys.argv[1])
    encoding = str(sys.argv[2])
    for path in sys.argv[3:]:
        paths.append(path)
    while True:
        buffer = input('Entrez un mot, le nombre de synonymes que vous voulez et la methode de calcul,\n'
                       ' i.e. produit scalaire: 0, least-squares:1, city-block:2\n\n'
                       'Tapez q pour quitter.\n')
        if buffer == 'q':
            quit()
        else:
            target_word, result_nb, method = buffer.split()
        trainer = t.Trainer(target_word, int(result_nb), window, encoding, paths)
        results = trainer.training(int(method))
        print('\n')
        for result in results:
            print(result[0] + ' --> ' + str(result[1]))
        print('\n')


if __name__ == '__main__':
    main()
