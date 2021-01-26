import copy
import threading
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import random

from PyQt5.QtCore import pyqtSignal, QObject

from cloud.Client import Client
from cloud.File import File

file_speed_transfer = 1000


def upload_worker(thread_ids, uploading_clients, upload_lock, *callbacks):
    thread_id = None
    with upload_lock:
        client_id, file = make_auction(uploading_clients)
        thread_id = thread_ids.pop()

        # uploading_clients_changed
        callbacks[0][0].emit()
        # thread_stared_upload
        callbacks[0][1].emit(thread_id, client_id, file)

    # writing file simulation
    time.sleep(file.size / file_speed_transfer)
    # thread_ended_upload
    callbacks[0][2].emit(thread_id)
    thread_ids.append(thread_id)


def make_auction(clients):
    print("auction")

    # counting weights
    weights = []
    for client in clients:
        weight = 0

        for file in client.files:
            weight = weight + np.reciprocal(file.size / file_speed_transfer)
        weight = weight + client.count_waited_time() - client.won_auction_times

        weights.append(weight)

    chosen_client_index = np.argmax(np.array(weights))
    chosen_client = clients[chosen_client_index]

    chosen_client.won_auction_times = chosen_client.won_auction_times + 1
    client_id, file = chosen_client.client_id, chosen_client.files.pop()
    return client_id, file


def upload_observer_worker(upload_event, threads_number, uploading_clients, *callbacks):
    # while not auction_event.isSet():
    while upload_event.wait():

        print("upload started")

        upload_lock = threading.Lock()
        # with ThreadPoolExecutor(threads_number) as executor:
        executor = ThreadPoolExecutor(threads_number)
        futures = []
        threads_indexes = list(range(threads_number))
        while len(uploading_clients) > 0 or len(futures) > 0:

            # remove done futures
            for i, future in enumerate(futures):
                if future.done() is True:
                    futures.pop(i)

            # remove empty clients
            for i, client in enumerate(uploading_clients):
                if len(client.files) is 0:
                    uploading_clients.pop(i)

            if len(futures) < threads_number and len(uploading_clients) > 0:
                future = executor.submit(upload_worker, threads_indexes, uploading_clients, upload_lock, callbacks)
                futures.append(future)

        print("upload ended")

        upload_event.clear()


class Cloud(QObject):
    uploading_clients_changed = pyqtSignal()
    thread_stared_upload = pyqtSignal(int, int, File)
    thread_ended_upload = pyqtSignal(int)

    def __init__(self, threads_number=5):
        super().__init__()

        self._threads_number = threads_number
        self.uploading_clients = []
        self.number_uploaded_clients = 0

        self.upload_thread = None
        self.upload_event = threading.Event()

        # self.uploading_clients_changed = None
        # self.thread_stared_upload = None
        # self.thread_ended_upload = None

    def start(self):
        self.upload_thread = threading.Thread(target=upload_observer_worker,
                                              args=(self.upload_event, self._threads_number,
                                                    self.uploading_clients, self.uploading_clients_changed,
                                                    self.thread_stared_upload, self.thread_ended_upload))
        self.upload_thread.daemon = True
        self.upload_thread.start()

    def upload_files(self, files):
        self.number_uploaded_clients = self.number_uploaded_clients + 1
        client = Client(self.number_uploaded_clients)

        client.files = files
        self.uploading_clients.append(client)

        self.upload_event.set()
        return client
