import threading


class SThread(threading.Thread):
    def __init__(self, method, args):
        threading.Thread.__init__(self)
        self.name = args[0].code
        self.method = method
        self.args = args

    def run(self):
        length = len(self.args)
        if length == 1:
            self.method(self.args[0])
        elif length == 2:
            self.method(self.args[0], self.args[1])
        elif length == 3:
            self.method(self.args[0], self.args[1], self.args[2])
