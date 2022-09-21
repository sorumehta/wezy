import time


class Buffer:
    def __init__(self):
        self.n_tries = 0
        self.stream = None
        self.contents = None
        self.buffered = 0
        self.start_time = time.time()
        self.request = None
        self.expecting = 0

    def read_buffer(self):
        pass