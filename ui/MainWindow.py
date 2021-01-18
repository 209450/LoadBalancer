from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow

from ui.WidgetFromFile import WidgetFromFile


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.config_parser = WidgetFromFile.load_config_parser()
        WidgetFromFile.load_ui(self, self.config_parser["MainWindow"]['ui_path'])

        self.client_table_model = QStandardItemModel()
        self.init_client_table_view()

    def init_client_table_view(self):
        labels = self.config_parser["MainWindow"]["client_view_headers"].split()
        self.client_table_model.setHorizontalHeaderLabels(labels)
        self.clientTableView.setModel(self.client_table_model)

        item = QStandardItem("aaa")
        item1 = QStandardItem("bbb")
        self.client_table_model.appendRow([item, item1])
