from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIntValidator
from PyQt5.QtWidgets import QMainWindow

from ui.WidgetFromFile import WidgetFromFile


class MainWindow(QMainWindow):

    def __init__(self, model, controller):
        super().__init__()
        self.model = model
        self.controller = controller
        self.config_parser = WidgetFromFile.load_config_parser()
        WidgetFromFile.load_ui(self, self.config_parser["MainWindow"]['ui_path'])

        self.client_table_model = QStandardItemModel()
        self.init_client_table_view()
        self.init_add_random_client_form()
        self.controller.start_cloud()

        self.model.uploading_clients_changed.connect(self.update_client_table_model)
        # self.model.uploading_clients_changed = self.eee

    def init_client_table_view(self):
        self.init_client_table_view_headers()
        self.clientTableView.setModel(self.client_table_model)

    def init_client_table_view_headers(self):
        labels = self.config_parser["MainWindow"]["client_view_headers"].split()
        self.client_table_model.setHorizontalHeaderLabels(labels)

    def init_add_random_client_form(self):
        self.minFileNumberLineEdit.setValidator(QIntValidator(1, 1000000))
        self.maxFileNumberLineEdit.setValidator(QIntValidator(1, 1000000))
        self.minFileSizeLineEdit.setValidator(QIntValidator(1, 1000000))
        self.maxFileSizeLineEdit.setValidator(QIntValidator(1, 1000000))
        self.addRandomClientPushButton.clicked.connect(self.add_random_client_push_button_handler)

    def add_random_client_push_button_handler(self):
        min_files = int(self.minFileNumberLineEdit.text())
        max_files = int(self.maxFileNumberLineEdit.text())
        min_size = int(self.minFileSizeLineEdit.text())
        max_size = int(self.maxFileSizeLineEdit.text())

        client = self.controller.random_upload(min_files, max_files, min_size, max_size)
        self.update_client_table_model()

    @pyqtSlot()
    def update_client_table_model(self):
        table_model = self.client_table_model
        clients = self.controller.uploading_clients

        table_model.clear()
        self.init_client_table_view_headers()
        for i, client in enumerate(clients):
            client_id = QStandardItem(str(client.client_id))
            files = QStandardItem(' '.join([str(i) for i in client.files]))
            table_model.setItem(i, 0, client_id)
            table_model.setItem(i, 1, files)
