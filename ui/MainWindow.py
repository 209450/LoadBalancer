from PyQt5.QtWidgets import QMainWindow

from ui.WidgetFromFile import WidgetFromFile


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.config_parser = WidgetFromFile.load_config_parser()
        WidgetFromFile.load_ui(self, self.config_parser["MainWindow"]['ui_path'])
