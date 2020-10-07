import sys
import time
import trainer as t
import reader as r
import processor as pr
import chrono as ch
import argparse
from pathlib import Path

def main():
    paths = []
    window = int(sys.argv[1])
    encoding = str(sys.argv[2])
    for path in sys.argv[3:]:
        paths.append(path)

    trainer = t.Trainer("jambe", window, encoding, paths)
    trainer.training(2)


if __name__ == '__main__':
    main()
