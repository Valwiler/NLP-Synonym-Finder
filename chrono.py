import time


class Chrono:

    def __init__(self):
        self.start_stamp = 0
        self.end_stamp = 0

    def start(self):
        self.start_stamp = time.time()

    def end(self):
        self.end_stamp = time.time()

    def log(self, message):
        print(message + str(self.end_stamp - self.start_stamp))

    def time_function(self, function, message):
        function()
