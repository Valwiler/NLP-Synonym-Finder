import sys
import trainer as t


# path C:\Users\mero1\Documents\Fall 2020\B51\b51-tp1\textes\GerminalUTF8.txt

def main():
    window = int(sys.argv[1])
    encoding = str(sys.argv[2])
    paths = []
    for path in sys.argv[3:]:
        paths.append(path)



if __name__ == '__main__':
    main()