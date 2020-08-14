# Python Imports
import logging
import traceback

# PyQt5 Imports
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox

# Own Imports
from kmap import __directory__, __version__
from kmap.controller.databasewindow import DatabaseWindow
from kmap.controller.tabwidget import TabWidget
from kmap.model.mainwindow_model import MainWindowModel
from kmap.config.config import config


# Load .ui File
UI_file = __directory__ + '/ui/mainwindow.ui'
MainWindow_UI, _ = uic.loadUiType(UI_file)


class MainWindow(QMainWindow, MainWindow_UI):

    def __init__(self):

        # Setup GUI
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self._setup()
        self._connect()

        self.model = MainWindowModel(self)

        self.open_welcome()

    def load_hdf5_files(self):
        # Load one or more new hdf5 files

        log = logging.getLogger('kmap')
        log.info('Loading .hdf5 file(s)...')

        start_path = __directory__ + config.get_key('paths', 'hdf5_start')
        extensions = 'hdf5 files (*.hdf5 *.h5);; All Files (*)'
        paths, _ = QFileDialog.getOpenFileNames(
            None, 'Open file(s)', start_path, extensions)

        if not paths:
            # No file chosen
            log.info('No file chosen')
            return

        for path in paths:

            self.tab_widget.open_sliced_data_tab(path)

    def open_database_browser(self):

        self.database = DatabaseWindow()
        self.database.files_chosen.connect(self.load_cube_files_online)

    def load_cube_files_online(self, URLs):

        if not URLs:
            # No file chosen
            logging.getLogger('kmap').info('No file chosen')
            return

        # Get Tab to load to
        tab = self.tab_widget.get_orbital_tab_to_load_to()

        # Load URL to Tab
        for URL in URLs:

            try:
                tab.add_orbital_from_online(URL[0], URL[1])

            except ValueError:
                logging.getLogger('kmap').error(
                    'URL "%s" is invalid. File could not be loaded.' % URL)

    def load_cube_files_locally(self):
        # Load one or more new cube files

        start_path = __directory__ + config.get_key('paths', 'cube_start')
        extensions = 'cube files (*.cube);; All Files (*)'
        paths, _ = QFileDialog.getOpenFileNames(
            None, 'Open file(s)', start_path, extensions)

        if not paths:
            # No file chosen
            logging.getLogger('kmap').info('No file chosen')
            return

        # Get Tab to load to
        tab = self.tab_widget.get_orbital_tab_to_load_to()

        # Load Data to Tab
        for path in paths:
            tab.add_orbital_from_filepath(path)

    def open_log_file(self):
        # Open log file

        path = __directory__ + '/../default.log'
        title = 'Log File'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=False)

    def open_mod_log_file(self):
        # Open module log file

        path = __directory__ + '/../modules.log'
        title = 'Modules Log File'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=False)

    def open_general_settings(self):
        # Open general user settings

        path = __directory__ + '/config/settings_user.ini'
        title = 'General Settings'

        self.tab_widget.open_file_tab(
            path, title, editable=True, richText=False)

    def open_orbital_data_tab(self):

        self.tab_widget.open_orbital_data_tab()
        
    def open_logging_settings(self):
        # Open logging user settings

        path = __directory__ + '/config/logging_user.ini'
        title = 'Logging Settings'

        self.tab_widget.open_file_tab(
            path, title, editable=True, richText=False)

    def open_general_default_settings(self):
        # Open general default settings

        path = __directory__ + '/config/settings_default.ini'
        title = 'General Settings (Default)'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=False)

    def open_logging_default_settings(self):
        # Open logging default settings

        path = __directory__ + '/config/logging_default.ini'
        title = 'Logging Settings (Default)'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=False)

    def open_readme(self):
        # Open a README page

        path = __directory__ + '/resources/texts/readme.txt'
        title = 'README'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=True)

    def open_welcome(self):
        # Open a welcome page

        path = __directory__ + '/resources/texts/welcome.txt'
        title = 'Welcome'

        self.tab_widget.open_file_tab(
            path, title, editable=False, richText=True)

    def open_about(self):
        # Open an about window

        path = __directory__ + '/resources/texts/about.txt'
        title, text = self.model.get_about_text(path)
        QMessageBox.about(self, title, text)

    def open_in_matplotlib(self):

        current_tab = self.tab_widget.get_current_tab()
        if hasattr(current_tab, 'display_in_matplotlib'):
            current_tab.display_in_matplotlib()

    def reload_settings(self):
        # Reload the settings

        config.setup()

    def _setup(self):

        self._set_misc()
        self._initialize_shortcuts()

    def _set_misc(self):

        x = int(config.get_key('app', 'x'))
        y = int(config.get_key('app', 'y'))
        w = int(config.get_key('app', 'w'))
        h = int(config.get_key('app', 'h'))
        self.setGeometry(x, y, h, w)
        if config.get_key('app', 'fullscreen') == 'True':
            self.showMaximized()
        self.setWindowTitle('kMap')
        self.setWindowIcon(
            QIcon(__directory__ + '/resources/images/icon.png'))
        self.show()

    def _initialize_shortcuts(self):

        actions = [self.load_hdf5_action, self.show_matplotlib,
                   self.log_file_action, self.load_cube_online_action,
                   self.load_cube_file_action]

        alias = ['load_hdf5', 'show_matplotlib', 'open_log',
                 'load_cube_online', 'load_cube_file']

        for action, alias in zip(actions, alias):
            shortcut = config.get_key('shortcut', alias, file='shortcut')
            action.setShortcut(QKeySequence(shortcut))

        self.ref_action.setShortcut(QKeySequence('Ctrl+r'))

    def _connect(self):

        # File menu
        self.load_hdf5_action.triggered.connect(self.load_hdf5_files)
        self.load_cube_file_action.triggered.connect(
            self.load_cube_files_locally)
        self.load_cube_online_action.triggered.connect(
            self.open_database_browser)
        self.log_file_action.triggered.connect(self.open_log_file)
        self.mod_log_file_action.triggered.connect(self.open_mod_log_file)
        self.show_matplotlib.triggered.connect(self.open_in_matplotlib)

        # Edit menu
        self.open_sim_tab_action.triggered.connect(self.open_orbital_data_tab)

        # Preferences menu
        self.general_action.triggered.connect(self.open_general_settings)
        self.logging_action.triggered.connect(self.open_logging_settings)
        self.general_default_action.triggered.connect(
            self.open_general_default_settings)
        self.logging_default_action.triggered.connect(
            self.open_logging_default_settings)
        self.settings_action.triggered.connect(self.reload_settings)

        # Help menu
        self.readme_action.triggered.connect(self.open_readme)
        self.welcome_action.triggered.connect(self.open_welcome)
        self.about_action.triggered.connect(self.open_about)