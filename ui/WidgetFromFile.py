import configparser

from PyQt5 import uic


class WidgetFromFile:
    __config_parser_path = "ui/config.ini"

    @staticmethod
    def load_ui(parent, ui_path):
        uic.loadUi(ui_path, parent)

    @staticmethod
    def load_config_parser():
        config = configparser.ConfigParser()
        config.read(WidgetFromFile.__config_parser_path)
        return config
