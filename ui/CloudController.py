import random

from cloud.File import File

names = "abcdef"


class CloudController:
    def __init__(self, model):
        self.model = model

    def start_cloud(self):
        self.model.start()

    def random_upload(self, max_files, min_size, max_size):
        files_number = random.randint(1, max_files)

        files = []
        for i in range(files_number):
            name = names[random.randint(0, len(names) - 1)]
            size = random.randint(min_size, max_size)
            files.append(File(name, size))

        self.model.upload_files(files)
        return self.model.number_uploaded_clients, files
