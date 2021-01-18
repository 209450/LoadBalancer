import sys

from cloud.Cloud import Cloud
from ui.CloudController import CloudController
from ui.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication


class App(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        cloud_model = Cloud()
        cloud_controller = CloudController(cloud_model)
        main_window = MainWindow(cloud_model, cloud_controller)
        main_window.show()
        self.main_window = main_window


if __name__ == "__main__":

    app = App(sys.argv)
    print("eee")
    sys.exit(app.exec_())
