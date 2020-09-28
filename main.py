import sys
import time
import trainer as t


def main():
    paths = []
    window = int(sys.argv[1])
    encoding = str(sys.argv[2])
    for path in sys.argv[3:]:
        paths.append(path)
    t0 = time.time()
    trainer = t.trainer(window, encoding, paths)
    print(time.time() - t0)


if __name__ == '__main__':
    main()
