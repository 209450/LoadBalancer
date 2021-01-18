import time

from cloud.File import File


class Client:

    def __init__(self, client_id):
        self.client_id = client_id
        self.files = []

        self.waited_time = time.time()
        self.won_auction_times = 0

    def count_waited_time(self):
        return time.time() - self.waited_time
