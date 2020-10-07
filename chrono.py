import time


class Chrono:
    def __init__(self):
        self.start_stamp = 0
        self.logs = list()

    # starts timer
    def start(self):
        self.start_stamp = time.time()

    # clock time and message
    def log(self, message):
        self.logs.append(Log(message))

    # clock endtime and pring clock list
    def end(self):
        self.logs.append(Log('Fin'))
        for log in self.logs:
            log.print_log(self.start_stamp)


class Log:
    def __init__(self, message):
        self.message = message
        self.timestamp = time.time()

    def print_log(self, start_time):
        print(self.message + " : " + str(self.timestamp - start_time))
