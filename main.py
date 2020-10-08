import sys
#import chron
import trainer as t

# Loop principale du programme

def main():
        paths = []
        window = int(sys.argv[1])
        encoding = sys.argv[2]
        for path in sys.argv[3:]:
            paths.append(path)
        while True:
            buffer = input('\nEntrez un mot, le nombre de synonymes que vous voulez et la methode de calcul.\n'
                           '( i.e. produit scalaire: 0, least-squares:1, city-block:2 )\n\n'
                           '\t\t\t\t\t\t\t Tapez q pour quitter.\n\n\t')
            if buffer == 'q':
                quit()
            else:
                target_word, result_nb, method = buffer.split()
            #check for target word here
            trainer = t.Trainer(target_word, int(result_nb), window, encoding, paths)
            results = trainer.training(int(method))
            print('\n')
            for result in results:
                print(result[0] + ' --> ' + str(result[1]))
            print('\n')


if __name__ == '__main__':
    main()
