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
    QTreeView,
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

        self.setWindowTitle(
            f"GameArt - {importlib.metadata.version('gameart')}"
        )
        self.resize(750, 500)

        menu_bar = self.menuBar()
        self._create_actions()
        menu_bar.addMenu(self._menu_bar())  # type: ignore

        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.main_tab = QWidget()
        self._setup_main_tab()
        self.tabWidget.addTab(self.main_tab, "Record and Generate")

    def _create_actions(self):
        """Creating action using the first constructor."""
        self.output_folder_action = QAction(self)
        self.output_folder_action.setText("&Select Output Folder")
        self.output_folder_action.triggered.connect(self._select_output_folder)

    def _menu_bar(self):
        """Create the menu bar."""
        file_menu = QMenu("&File", self)
        file_menu.addAction(self.output_folder_action)

        return file_menu

    def _setup_main_tab(self):
        """Create the main page."""
        layout = QGridLayout()

        # Create buttons
        btn_start_record = QPushButton("Start Recording")
        btn_start_record.clicked.connect(self._execute_record)
        layout.addWidget(btn_start_record, 2, 0, 3, 0)

        btn_generate_image = QPushButton("Generate Image")
        btn_generate_image.clicked.connect(self._execute_draw)
        layout.addWidget(btn_generate_image, 5, 0, 6, 0)

        # Create file system models (dir and files)
        self.dir_model = QFileSystemModel()
        self.dir_model.setRootPath(QDir.rootPath())
        self.dir_model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.file_model.setFilter(QDir.NoDotAndDotDot | QDir.Files)
        self.file_model.setNameFilters(["*.csv"])

        # Create tree and list view
        tree_view = QTreeView()
        tree_view.setModel(self.dir_model)
        tree_view.setRootIndex(
            self.dir_model.index(str(self.file_handler.output_path))
        )
        tree_view.clicked.connect(self._on_tree_view_clicked)
        layout.addWidget(tree_view, 1, 0)

        self.list_view = QListView()
        self.list_view.setModel(self.file_model)
        self.list_view.setRootIndex(
            self.file_model.index(str(self.file_handler.output_path))
        )
        self.list_view.clicked.connect(self._on_list_view_clicked)
        layout.addWidget(self.list_view, 1, 1)

        self.main_tab.setLayout(layout)

    def _on_tree_view_clicked(self, index):
        folder_path = self.dir_model.fileInfo(index).absoluteFilePath()
        logging.info("Folder selected %s" % (folder_path))
        self.list_view.setRootIndex(self.file_model.setRootPath(folder_path))

    def _on_list_view_clicked(self, index):
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        logging.info("File selected %s" % (file_path))
        self.file_handler.csv_file = file_path

    def _select_output_folder(self):
        output_folder = QFileDialog.getExistingDirectory(
            self, "Select Output Folder"
        )
        if output_folder:
            self.file_handler.output_path = Path(output_folder)
            logging.info("Folder selected %s" % (output_folder))
        else:
            logging.warn("No output folder selected!")

    def _execute_record(self):
        record_mouse()

    def _execute_draw(self):
        draw_mouse_tracks()


def start_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
