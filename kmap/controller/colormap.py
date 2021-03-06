# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDir

# Own Imports
from kmap import __directory__
from kmap.model.colormap_model import ColormapModel
from kmap.config.config import config

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/colormap.ui')
Colormap_UI, _ = uic.loadUiType(UI_file)


class Colormap(QWidget, Colormap_UI):

    def __init__(self, plot_item):

        # Setup GUI
        super(Colormap, self).__init__()
        self.setupUi(self)
        self._connect()

        # Path for the .json file containing the colormaps
        self.path = __directory__ + config.get_key('paths', 'colormap')
        self.model = ColormapModel(plot_item)

        self.load_colormaps()

    def load_colormaps(self):

        try:
            self.model.load_colormaps(self.path)

        except Exception:

            log = logging.getLogger('kmap')

            log.error('Colormaps could not be loaded')
            log.error(traceback.format_exc())

        self._update_combobox()
        self.set_default_colormap()

    def add_colormap(self):

        name = self.line_edit.text()

        if name:
            self.model.add_colormap_from_plot(name)
            self._update_combobox()
            self.set_colormap(name)

    def remove_colormap(self):

        name = self.combobox.currentText()

        if name:
            self.model.remove_colormap(name)
            self._update_combobox()
            self.set_default_colormap()

    def save(self):

        try:
            self.model.save_colormaps(self.path)

        except Exception:

            log = logging.getLogger('kmap')

            log.error('Colormaps could not be saved')
            log.error(traceback.format_exc())

            os.remove(path_temp)

    def set_colormap(self, name):

        self.model.set_current_colormap(name)
        self.combobox.setCurrentText(name)

    def set_default_colormap(self):

        default_colormap = config.get_key('colormap', 'default')
        self.set_colormap(default_colormap)

    def _update_combobox(self):

        self.combobox.blockSignals(True)

        self.combobox.clear()
        for colormap in self.model.colormaps:
            self.combobox.addItem(colormap.name)

        self.combobox.blockSignals(False)

    def _connect(self):

        self.combobox.currentTextChanged.connect(self.set_colormap)
        self.remove_button.clicked.connect(self.remove_colormap)
        self.add_button.clicked.connect(self.add_colormap)
        self.save_button.clicked.connect(self.save)
        self.reload_button.clicked.connect(self.load_colormaps)
