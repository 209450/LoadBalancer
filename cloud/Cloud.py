import threading


class Cloud:
    def __init__(self, threads_number=5, client_list=[]):
        self._threads_number = threads_number
        self._client_list = client_list

