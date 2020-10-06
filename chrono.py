import time


class Chrono:

    def __init__(self):
        self.start_stamp = 0
        self.logs = list()

    def start(self):
        self.start_stamp = time.time()

    def end(self):
        self.logs.append(time.time())
        for i,timestamp in enumerate(self.logs):
            print("#"+str(i) + " :" + str(self.start_stamp - timestamp))

    def log(self):
        self.logs.append(time.time())

