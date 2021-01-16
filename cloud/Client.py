from cloud.File import File


class Client:

    def __init__(self, client_id):
        self.client_id = client_id
        self.files = []

        self.waited_time = 0


