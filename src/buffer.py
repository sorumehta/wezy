import time


class Buffer:
    def __init__(self, stream_data):
        self.n_tries = 0
        self.contents = None
        self.bi_stream = stream_data
        self.total_buffered = 0
        self.start_time = time.time()
        self.request = None
        self.expecting = 0


    def process_buffer(self):
        pass