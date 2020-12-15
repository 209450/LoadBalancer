import configparser

from PyQt5 import uic


class WidgetFromFile:
    def load_UI(self, ui_path):
        uic.loadUi(ui_path, self)

    def load_config_parser(self, config_parser_path):
        config = configparser.ConfigParser()
        config.read(config_parser_path)
        return config
