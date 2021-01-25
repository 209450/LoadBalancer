import random

from cloud.File import File

names = "abcdef"


class CloudController:
    def __init__(self, model):
        self.model = model
        self.uploading_clients = model.uploading_clients

    def start_cloud(self):
        self.model.start()

    def random_upload(self, min_files, max_files, min_size, max_size):
        files_number = random.randint(min_files, max_files)

        files = []
        for i in range(files_number):
            name = names[random.randint(0, len(names) - 1)]
            size = random.randint(min_size, max_size)
            files.append(File(name, size))

        return self.model.upload_files(files)
