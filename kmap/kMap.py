import os
import logging
import logging.config

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDir

import pyqtgraph as pg

from kmap.config.config import config
from kmap.controller.mainwindow import MainWindow
from kmap import __version__, __project__, __directory__


class kMap(QApplication):

    def __init__(self, sysarg):

        # Apply various configurations
        self.load_settings(startup=True)

        logging.getLogger('kmap').debug(
            'Initializing kMap.py v' + __version__ + '.')

        # Initialize application
        super().__init__(sysarg)
        self.setApplicationVersion(__version__)
        self.setApplicationName(__project__)
        self.setDesktopFileName(__project__)

    def run(self):

        logging.getLogger('kmap').info('Starting up kMap.')

        # Creating mainwindow
        self.main_window = MainWindow()

        super().exec_()

    def test(self):
        pass

    def load_settings(self, startup=False):

        # Logging
        # Delete old log files if user set to do so
        if startup and config.get_key('logging', 'persistent') == 'False':
            log_file = __directory__ + \
                QDir.toNativeSeparators('/../default.log')
            if os.path.exists(log_file):
                os.remove(log_file)

        logging.config.fileConfig(config.get_config(
            'logging'), disable_existing_loggers=False)

        # PyQtGraph
        value = config.get_key('pyqtgraph', 'background')
        if value == 'None':
            pg.setConfigOption('background', None)

        else:
            pg.setConfigOption('background', value)

        value = config.get_key('pyqtgraph', 'foreground')
        if value == 'None':
            pg.setConfigOption('foreground', None)

        else:
            pg.setConfigOption('foreground', value)

        value = config.get_key('pyqtgraph', 'antialias')
        if value == 'True':
            pg.setConfigOption('antialias', True)

        else:
            pg.setConfigOption('antialias', False)

        value = config.get_key('pyqtgraph', 'imageAxisOrder')
        pg.setConfigOption('imageAxisOrder', value)

        self.setFont(QFont(config.get_key('font', 'font'), int(
            config.get_key('font', 'size')), QFont.Normal))

        logging.getLogger('kmap').debug('Settings loaded successfully.')
