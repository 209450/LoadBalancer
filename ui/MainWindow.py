from PyQt5.QtWidgets import QMainWindow

from ui.WidgetFromFile import WidgetFromFile


class MainWindow(QMainWindow, WidgetFromFile):
    __config_parser_path = "ui/config.ini"

    def __init__(self):
        super().__init__()
        self.config_parser = self.load_config_parser(self.__config_parser_path)
        print(self.config_parser["MainWindow"]['ui_path'])
