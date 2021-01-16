import threading
import time
from concurrent.futures import ThreadPoolExecutor
import random

from cloud.Client import Client


def upload_worker(thread_id, client_id, file, upload_lock):
    with upload_lock:
        print(f"Thread {thread_id}: start, client_id: {client_id}, uploading: {file}")

    # writing file simulation
    time.sleep(2 * random.random())
    print(f"Thread {thread_id}: end")


def auction_worker(auction_event, threads_number, uploading_clients):
    # while not auction_event.isSet():
    while auction_event.wait():

        print("auction started")

        upload_lock = threading.Lock()
        while len(uploading_clients) is not 0:
            with ThreadPoolExecutor(threads_number) as executor:
                for i in range(len(uploading_clients)):
                    # client_id, file = make_auction(client_dict, client_files, uploading_clients_ids)

                    client = uploading_clients.pop()
                    client_id, file = client.client_id, client.files
                    executor.submit(upload_worker, i, client_id, file, upload_lock)

        print("auction ended")

        auction_event.clear()


def make_auction(client_dict, client_files, uploading_clients_ids):
    now_uploading_files_with_weights = {}
    for uploading_client_id in uploading_clients_ids:
        user_files_to_upload = client_dict[uploading_client_id] - client_files[uploading_client_id]
        files_with_weights = {file: file.size / 1000 for file in user_files_to_upload}

        now_uploading_files_with_weights[uploading_client_id] = files_with_weights

    client_id = uploading_clients_ids.pop()
    file = client_dict[client_id] - client_files[client_id]
    return client_id, file


class Cloud:
    def __init__(self, threads_number=5):
        self._threads_number = threads_number
        self._uploading_clients = []

        self.auction_event = threading.Event()

    def start_cloud(self):
        executor = ThreadPoolExecutor()
        executor.submit(auction_worker, self.auction_event, self._threads_number, self._uploading_clients)

    def upload_files(self, files):
        client_id = len(self._uploading_clients)
        client = Client(client_id)

        client.files = files
        self._uploading_clients.append(client)

        self.auction_event.set()
