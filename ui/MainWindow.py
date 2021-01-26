from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIntValidator, QPalette
from PyQt5.QtWidgets import QMainWindow, QWidget

from cloud.File import File
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
        self.model.thread_stared_upload.connect(self.update_thread_widget_on_thread_start_upload)
        self.model.thread_ended_upload.connect(self.update_thread_widget_on_thread_stop_upload)

        self.threads_widgets = {}
        self.init_threads_widgets()
        print(self.threads_widgets)

    def init_threads_widgets(self):
        layout = self.cloudGroupBox.layout()
        threads = self.threads_widgets

        threads_number = int(self.config_parser["MainWindow"]["threads_widgets"])
        for i in range(threads_number):
            thread_widget = ThreadWidget(f"Wątek {i}")
            threads[i] = thread_widget
            layout.addWidget(thread_widget)

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

    @pyqtSlot(int, int, File)
    def update_thread_widget_on_thread_start_upload(self, thread_id, client_id, file):
        # print(f"Thread {thread_id}: start, client_id: {client_id}, uploading: {file}")
        print(thread_id)
        thread_widget = self.threads_widgets[thread_id]
        thread_widget.fill_form(client_id, file.name, file.size)

    @pyqtSlot(int)
    def update_thread_widget_on_thread_stop_upload(self, thread_id):
        # print(f"Thread {thread_id}: end")
        thread_widget = self.threads_widgets[thread_id]
        thread_widget.free_from()


class ThreadWidget(QWidget):
    def __init__(self, title, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config_parser = WidgetFromFile.load_config_parser()
        WidgetFromFile.load_ui(self, self.config_parser["ThreadWidget"]['ui_path'])

        self.threadGroupBox.setTitle(title)
        self.free_from()

    def fill_form(self, client_id, file_name, file_size):
        self.statusQLable.setText("Zajęty")
        self.change_label_color(self.statusQLable, Qt.red)

        self.userLineEdit.setText(str(client_id))
        self.fileLineEdit.setText(file_name)
        self.sizeLineEdit.setText(str(file_size))

    def free_from(self):
        self.statusQLable.setText("Wolny")
        self.change_label_color(self.statusQLable, Qt.darkGreen)

        self.userLineEdit.clear()
        self.fileLineEdit.clear()
        self.sizeLineEdit.clear()

    def change_label_color(self, label, color):
        pallete = QPalette()
        pallete.setColor(QPalette.WindowText, color)
        label.setPalette(pallete)
