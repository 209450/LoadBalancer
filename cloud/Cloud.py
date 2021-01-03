import threading
import time
from concurrent.futures import ThreadPoolExecutor
import random

from cloud.Client import Client


def upload_worker(name, uploading_clients, upload_lock):
    with upload_lock:
        print(f"Thread {name}: start")
        print(f"Popped: {uploading_clients.pop()}")
    time.sleep(2 * random.random())
    print(f"Thread {name}: end")


def auction_worker(uploading_clients, threads_number, auction_event):
    # while not auction_event.isSet():
    while auction_event.wait():

        print("auction started")
        a = threading.Lock()
        index = 0
        while len(uploading_clients) is not 0:
            with ThreadPoolExecutor(threads_number) as executor:
                for i in range(len(uploading_clients)):
                    executor.submit(upload_worker, i, uploading_clients, a)
                    index += 1
        print("auction ended")

        auction_event.clear()


def make_auction():
    pass


class Cloud:
    def __init__(self, threads_number=5):
        self._threads_number = threads_number
        self._client_dict = {}
        self._client_files = {}

        self.auction_event = threading.Event()
        self.uploading_clients = set()
        self.upload_observer = UploadObserver(self.auction_event, self.uploading_clients)

    def start_cloud(self):
        # with ThreadPoolExecutor(self._threads_number) as executor:
        executor = ThreadPoolExecutor()
        # for index in range(self._threads_number):
        #     executor.submit(upload_worker, index, self.uploading_clients, self.upload_lock)

        executor.submit(auction_worker, self.uploading_clients, self._threads_number, self.auction_event)

    def add_client(self):
        client_id = len(self._client_dict)
        client = Client(client_id, self.upload_observer)

        self._client_dict[client_id] = client
        self._client_files[client_id] = []

        return client

    def get_client(self, id):
        return self._client_dict[id]


class UploadObserver:

    def __init__(self, auction_event, uploading_clients):
        self.auction_event = auction_event
        self.uploading_clients = uploading_clients

    def notify(self, client_id):
        self.uploading_clients.add(client_id)
        self.auction_event.set()
