import threading
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import random

from cloud.Client import Client


def upload_worker(thread_id, uploading_clients, upload_lock):
    with upload_lock:
        client_id, file = make_auction(uploading_clients)
        print(f"Thread {thread_id}: start, client_id: {client_id}, uploading: {file}")

    # writing file simulation
    time.sleep(2 * random.random())
    print(f"Thread {thread_id}: end")


def auction_worker(auction_event, threads_number, uploading_clients):
    # while not auction_event.isSet():
    while auction_event.wait():

        print("upload started")

        upload_lock = threading.Lock()
        with ThreadPoolExecutor(threads_number) as executor:
            futures = []
            while len(uploading_clients) > 0:

                # remove done futures
                for i, future in enumerate(futures):
                    if future.done() is True:
                        futures.pop(i)

                # remove empty clients
                for i, client in enumerate(uploading_clients):
                    if len(client.files) is 0:
                        uploading_clients.pop(i)

                if len(futures) < threads_number:
                    futures.append(executor.submit(upload_worker, 0, uploading_clients, upload_lock))

        print("upload ended")

        auction_event.clear()


def make_auction(clients):
    print("auction")

    # counting weights
    weights = []
    for client in clients:
        weight = 0

        weights.append(weight)

    chosen_client_index = np.argmax(np.array(weights))
    chosen_client = clients[chosen_client_index]

    client_id, file = chosen_client.client_id, chosen_client.files.pop()
    return client_id, file


class Cloud:
    def __init__(self, threads_number=5):
        self._threads_number = threads_number
        self._uploading_clients = []
        self.number_uploaded_clients = 0

        self.auction_event = threading.Event()

    def start_cloud(self):
        executor = ThreadPoolExecutor()
        executor.submit(auction_worker, self.auction_event, self._threads_number, self._uploading_clients)

    def upload_files(self, files):
        self.number_uploaded_clients = self.number_uploaded_clients + 1
        client = Client(self.number_uploaded_clients)

        client.files = files
        self._uploading_clients.append(client)

        self.auction_event.set()
