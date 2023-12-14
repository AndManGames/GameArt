import importlib.metadata
import logging
import sys
from pathlib import Path

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QFileSystemModel,
    QGridLayout,
    QListView,
    QMainWindow,
    QMenu,
    QPushButton,
    QTabWidget,
    QWidget,
)

from gameart.api import draw_mouse_tracks, record_mouse
from gameart.FileHandler import FileHandlerSingleton

logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    """Main Window."""

    def __init__(self):
        super().__init__()
        self.file_handler = FileHandlerSingleton()
        self._base_folder = str(self.file_handler.output_path)

        self.setWindowTitle(
            f"GameArt - {importlib.metadata.version('gameart')}"
        )
        self.resize(500, 500)

        menu_bar = self.menuBar()
        self._create_actions()
        menu_bar.addMenu(self._menu_bar())  # type: ignore

        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.main_tab = QWidget()
        self._setup_main_tab()
        self.tabWidget.addTab(self.main_tab, "Record and Generate")

    @property
    def base_folder(self):
        return self._base_folder

    @base_folder.setter
    def base_folder(self, value):
        self._base_folder = value

    def _create_actions(self):
        self.output_folder_action = QAction(self)
        self.output_folder_action.setText("&Select Output Folder")
        self.output_folder_action.triggered.connect(self._select_output_folder)

    def _menu_bar(self):
        file_menu = QMenu("&File", self)
        file_menu.addAction(self.output_folder_action)

        return file_menu

    def _setup_main_tab(self):
        layout = QGridLayout()

        # Create buttons
        btn_select_base_folder = QPushButton("Select Folder")
        btn_select_base_folder.clicked.connect(self._select_base_folder)
        layout.addWidget(btn_select_base_folder, 1, 0)

        btn_start_record = QPushButton("Start Recording")
        btn_start_record.clicked.connect(self._execute_record)
        layout.addWidget(btn_start_record, 3, 0)

        btn_generate_image = QPushButton("Generate Image")
        btn_generate_image.clicked.connect(self._execute_draw)
        layout.addWidget(btn_generate_image, 4, 0)

        # Create file system model
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.file_model.setFilter(QDir.NoDotAndDotDot | QDir.Files)
        self.file_model.setNameFilters(["*.csv"])

        # Create list view
        self.list_view = QListView()
        self.list_view.setModel(self.file_model)
        self._update_list_view(self.base_folder)
        self.list_view.clicked.connect(self._on_list_view_clicked)
        layout.addWidget(self.list_view, 2, 0)

        self.main_tab.setLayout(layout)

    def _update_list_view(self, folder):
        self.list_view.setRootIndex(self.file_model.setRootPath(folder))
        logging.info("List view updated.")

    def _on_list_view_clicked(self, index):
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        logging.info("File selected %s" % (file_path))
        self.file_handler.csv_file = file_path

    def _select_base_folder(self):
        self.base_folder = QFileDialog.getExistingDirectory(
            self, "Select Folder"
        )
        if self.base_folder:
            self._update_list_view(self.base_folder)
            logging.info("Folder selected %s" % (self.base_folder))
        else:
            logging.warn("No folder selected!")

    def _select_output_folder(self):
        output_folder = QFileDialog.getExistingDirectory(
            self, "Select Output Folder"
        )
        if output_folder:
            self.file_handler.output_path = Path(output_folder)
            logging.info("Output folder selected %s" % (output_folder))
        else:
            logging.warn("No output folder selected!")

    def _execute_record(self):
        record_mouse()
        self._update_list_view(self.base_folder)

    def _execute_draw(self):
        draw_mouse_tracks()
        self._update_list_view(self.base_folder)


def start_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
