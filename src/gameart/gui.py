import importlib.metadata
import logging
import sys
import webbrowser
from pathlib import Path

from PyQt5.QtCore import QDir, QModelIndex, Qt
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QFileSystemModel,
    QGridLayout,
    QLabel,
    QListView,
    QMainWindow,
    QMenu,
    QPushButton,
    QTabWidget,
    QWidget,
)

from gameart.api import draw_mouse_tracks, record_mouse
from gameart.FileHandler import FileHandlerSingleton


class MainWindow(QMainWindow):
    """
    Class of Main Window. Consists of a menu bar and a tab widget.
    It also uses the singleton file handler class of gameart to get and set the
    relevant paths. Class has the property base_folder to get and set the base
    folder which gets displayed in the list view.

    Args:
        QMainWindow (object): The QMainWindow class provides a main
        application window.
    """

    def __init__(self) -> None:
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
    def base_folder(self) -> str:
        return self._base_folder

    @base_folder.setter
    def base_folder(self, value: str):
        self._base_folder = value

    def _create_actions(self) -> None:
        """
        Creates actions for the menu bar buttons. Pressing the button
        "Select Output Folder" connects to the _select_output_folder method
        """
        self.output_folder_action = QAction(self)
        self.output_folder_action.setText("&Select Output Folder")
        self.output_folder_action.triggered.connect(self._select_output_folder)

    def _menu_bar(self) -> QMenu:
        """
        Creates the menus for the menu bar and connects the respective actions
        - File

        Returns:
            QMenu: Returns the PyQt5 QMenu object
        """
        file_menu = QMenu("&File", self)
        file_menu.addAction(self.output_folder_action)

        return file_menu

    def _setup_main_tab(self) -> None:
        """
        Sets up the main tab by creating buttons, file system and list view.
        It adds all relevant widgets to the layout of the tab.
        """
        layout = QGridLayout()

        # Create buttons
        btn_select_base_folder = QPushButton("Select Folder to View")
        btn_select_base_folder.clicked.connect(self._select_base_folder)
        layout.addWidget(btn_select_base_folder, 1, 0)

        btn_start_record = QPushButton("Start Recording")
        btn_start_record.clicked.connect(self._execute_record)
        layout.addWidget(btn_start_record, 3, 0)

        btn_generate_image = QPushButton("Generate Image")
        btn_generate_image.clicked.connect(self._execute_draw)
        layout.addWidget(btn_generate_image, 4, 0)

        btn_open_upload_page = QPushButton("Upload Image (coming soon)")
        btn_open_upload_page.clicked.connect(self._open_upload_page)
        btn_open_upload_page.setEnabled(False)
        layout.addWidget(btn_open_upload_page, 6, 0)

        # Create labels
        self.label_current_output_folder = QLabel(
            "label_current_output_folder"
        )
        self.label_current_output_folder.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self._update_output_folder_label(str(self.file_handler.output_path))
        layout.addWidget(self.label_current_output_folder, 5, 0)

        # Create file system model
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.file_model.setFilter(
            QDir.NoDotAndDotDot | QDir.Files | QDir.AllDirs
        )
        self.file_model.setNameFilters(["*.csv"])

        # Create list view
        self.list_view = QListView()
        self.list_view.setModel(self.file_model)
        self._update_list_view(self.base_folder)
        self.list_view.clicked.connect(self._on_list_view_clicked)
        layout.addWidget(self.list_view, 2, 0)

        self.main_tab.setLayout(layout)

    def _update_list_view(self, folder: str) -> None:
        """
        Updates the list view by setting the root index to the given folder
        path

        Args:
            folder (str): Path to the folder which shall be visible in list
            view
        """
        self.list_view.setRootIndex(self.file_model.setRootPath(folder))
        logging.info("List view updated.")

    def _update_output_folder_label(self, folder: str) -> None:
        """
        Updates the label of the current output folder by setting the text to
        the given folder path

        Args:
            folder (str): Path to the folder which shall be visible in label
            view
        """
        self.label_current_output_folder.setText(
            f"(Current output folder {folder}, File -> "
            + "Select Output Folder)"
        )
        logging.info("Label of output folder updated.")

    def _on_list_view_clicked(self, index: QModelIndex) -> None:
        """
        Gets the file path of the selected file and sets the csv_file property
        of the file handler class accordingly. If the file is not a .csv the
        method returns None.

        Args:
            index (QModelIndex): Index of the file which got selected in list
            view
        """
        file_extension = self.file_model.fileInfo(index).completeSuffix()
        if file_extension != "csv":
            logging.warning(
                "File extension .%s not supported!" % (file_extension)
            )
            return
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        logging.info("File selected %s" % (file_path))
        self.file_handler.csv_file = file_path

    def _select_base_folder(self) -> None:
        """
        Method to set the base folder of the list view. It updates the list
        view to display all files in that base folder
        """
        self.base_folder = QFileDialog.getExistingDirectory(
            self, "Select Folder"
        )
        if self.base_folder:
            self._update_list_view(self.base_folder)
            logging.info("Folder selected %s" % (self.base_folder))
        else:
            logging.warning("No folder selected!")

    def _select_output_folder(self) -> None:
        """
        Opens a file dialog to let the user select the output folder, where the
        gameart output folder will be created after generating the images.
        """
        output_folder = QFileDialog.getExistingDirectory(
            self, "Select Output Folder"
        )
        if output_folder:
            self.base_folder = output_folder
            self._update_output_folder_label(output_folder)
            self._update_list_view(output_folder)
            self.file_handler.output_path = Path(output_folder)
            logging.info("Output folder selected %s" % (output_folder))
        else:
            logging.warning("No output folder selected!")

    def _execute_record(self) -> None:
        """
        Executes the record mouse method and updates the list view afterwards.
        """
        record_mouse()
        self._update_list_view(self.base_folder)

    def _execute_draw(self) -> None:
        """
        Executes the draw method and updates the list view afterwards.
        """
        draw_mouse_tracks()
        self._update_list_view(self.base_folder)

    def _open_upload_page(self) -> None:
        """
        Opens the upload page of gameart_web
        """
        webbrowser.open("http://127.0.0.1:8000/dashboard/")


def _start_gui() -> None:
    """
    Starts the GUI.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


# entry point for pyinstaller
if __name__ == "__main__":
    _start_gui()
