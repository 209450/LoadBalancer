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

    def init_client_table_view(self):
        labels = self.config_parser["MainWindow"]["client_view_headers"].split()
        self.client_table_model.setHorizontalHeaderLabels(labels)
        self.clientTableView.setModel(self.client_table_model)

        # item = QStandardItem("aaa")
        # item1 = QStandardItem("bbb")
        # self.client_table_model.appendRow([item, item1])

    def init_add_random_client_form(self):
        self.maxFileNumberLineEdit.setValidator(QIntValidator(1, 1000000))
        self.minFileSizeLineEdit.setValidator(QIntValidator(1, 1000000))
        self.maxFileSizeLineEdit.setValidator(QIntValidator(1, 1000000))
        self.addRandomClientPushButton.clicked.connect(self.add_random_client_push_button_handler)

    def add_random_client_push_button_handler(self):
        max_files = int(self.maxFileNumberLineEdit.text())
        min_size = int(self.minFileSizeLineEdit.text())
        max_size = int(self.maxFileSizeLineEdit.text())

        client = self.controller.random_upload(max_files, min_size, max_size)
        item = QStandardItem(str(client.client_id))
        item1 = QStandardItem(' '.join([str(i) for i in client.files]))
        self.client_table_model.appendRow([item, item1])

        # print(self.client_table_model.findItems("1", 0))

