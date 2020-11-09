import argparse
import sys

class ArgvParser:
    _instance = None

    @staticmethod
    def getInstance():
        if ArgvParser._instance is None:
            ArgvParser()
        return ArgvParser._instance

    def __init__(self):
        if ArgvParser._instance is None:
            ArgvParser._instance = self
        
        self._parser = argparse.ArgumentParser()
        self._initArguments()
        if len(sys.argv) == 1: #[P.Q. 2020.11.07] No argument show help and exit
            self._parser.print_help()
            sys.exit()
        else:
            self.args = self._parser.parse_args()
    
    def _initArguments(self):
        args_group = self._parser.add_mutually_exclusive_group(required=True)

        args_group.add_argument('-e', '--entrainement', action='store_true',
            help='Start the application in Training mode. Cannot be used with -r argument.')
        args_group.add_argument('-r', '--recherche', action='store_true',
            help='Start the application in Research mode. Cannot be used with -e argument.')
        
        self._parser.add_argument('-t', '--taille', required=True, action='store', type=int, default=5,
            help='Size of the algorithm window used in training.')
        self._parser.add_argument('--encodage', '--enc', required='-e' in sys.argv, action='store', type=str, default='utf-8',
            help='Encoding of the files in --chemin. Required when training.')
        self._parser.add_argument('--chemin', required='--e' in sys.argv, action='store', nargs='+',
            help='List of files. Required when training')

    def isTrainingMode(self):
        return self.args.entrainement

    def isResearchMode(self):
        return self.args.recherche

    def windowSize(self):
        return self.args.taille

    def encoding(self):
        return self.args.encodage

    def filesPath(self):
        return self.args.chemin