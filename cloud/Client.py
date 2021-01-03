from cloud.File import File


class Client:

    def __init__(self, client_id, upload_observer):
        self.client_id = client_id
        self.upload_observer = upload_observer
        self.files = []

    def upload_file(self, name, size):
        new_file = File(name, size)
        self.files.append(new_file)
        self.upload_observer.notify(self.client_id)
