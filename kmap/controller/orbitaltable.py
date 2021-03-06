# Python Imports
import logging

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal, QDir
from PyQt5.QtWidgets import QWidget, QHeaderView, QHBoxLayout

# Own Imports
from kmap import __directory__
from kmap.controller.orbitaltablerow import OrbitalTableRow

# Load .ui File
UI_file = __directory__ + QDir.toNativeSeparators('/ui/orbitaltable.ui')
OrbitalTable_UI, _ = uic.loadUiType(UI_file)


class OrbitalTable(QWidget, OrbitalTable_UI):

    orbital_changed = pyqtSignal(int)
    orbital_removed = pyqtSignal(int)
    orbital_selected = pyqtSignal(int)

    def __init__(self, *args, **kwargs):

        # Setup GUI
        super(OrbitalTable, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._setup()

        self.rows = []

    def add_orbital(self, orbital, orientation):

        new_row = OrbitalTableRow(orbital, orientation)

        self._add_row(new_row)

    def remove_orbital_by_ID(self, ID):

        index = self._ID_to_row_index(ID)

        self.table.removeRow(index)
        del self.rows[index]

        self.orbital_removed.emit(ID)

    def get_parameters_by_ID(self, ID):

        index = self._ID_to_row_index(ID)

        return self.rows[index].get_parameters()

    def get_use_by_ID(self, ID):

        index = self._ID_to_row_index(ID)

        return self.rows[index].get_use()

    def change_parameter(self, ID, parameter, value):

        self._update_selected_rows(parameter, value)

        self.orbital_changed.emit(ID)

    def change_use(self, ID):

        self.orbital_changed.emit(ID)

    def _add_row(self, new_row):

        row_index = len(self.rows)

        self.rows.append(new_row)

        self.table.insertRow(row_index)
        self._embed_row(new_row, row_index)
        self._connet_row(new_row)
        # "Select" newly added row to trigger miniplots
        self.table.cellClicked.emit(row_index, 2)

    def _ID_to_row_index(self, ID):

        for index, row in enumerate(self.rows):
            if row.ID == ID:
                return index

        raise IndexError('No data with this ID')

    def _update_selected_rows(self, parameter, value):

        selected_rows = self.table.selectionModel().selectedIndexes()
        for selected_row in selected_rows:
            row = self.rows[selected_row.row()]
            row.update_parameter_silently(parameter, value)

    def _setup(self):

        widths = [40, 40, 0, 90, 80, 80, 80, 45]

        for col, width in enumerate(widths):
            self.table.setColumnWidth(col, width)

        self.table.horizontalHeader().setResizeMode(2, QHeaderView.Stretch)

    def _embed_row(self, row, row_index):

        # To center checkbox, embed it inside a layout inside a widget
        layout = QHBoxLayout()
        layout.addWidget(row.use)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        center_widget = QWidget()
        center_widget.setLayout(layout)

        widgets = [row.button, row.ID_label, row.name_label, row.weight,
                   row.phi, row.theta, row.psi, center_widget]

        for col, widget in enumerate(widgets):
            self.table.setCellWidget(row_index, col, widget)

    def _row_selected(self, row):

        self.orbital_selected.emit(self.rows[row].ID)

    def _connet_row(self, row):

        row.row_removed.connect(self.remove_orbital_by_ID)
        row.parameter_changed.connect(self.change_parameter)
        row.use_changed.connect(self.change_use)

        self.table.cellClicked.connect(self._row_selected)
