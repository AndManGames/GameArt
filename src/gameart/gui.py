import importlib.metadata
import logging
import sys
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from gameart.api import draw_mouse_tracks, record_mouse
from gameart.FileHandler import FileHandlerSingleton
from gameart.utils import utils

logging.basicConfig(level=logging.INFO)


screen_width = utils._get_screensize()[0]
screen_height = utils._get_screensize()[1]
window_width = screen_width // 5
window_height = screen_height // 3


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            f"GameArt - {importlib.metadata.version('gameart')}"
        )
        self.resize(270, 150)
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(
            QLabel(f"{importlib.metadata.metadata('gameart')['summary']}")
        )

        tabs = QTabWidget()
        tabs.addTab(self.main_tab(), "Record and Generate")
        tabs.addTab(self.manage_recordings_tab(), "My local recordings")
        layout.addWidget(tabs)
        layout.addStretch()

        self.file_handler = FileHandlerSingleton()

    def main_tab(self):
        """Create the main page."""
        mainTab = QWidget()
        layout = QVBoxLayout()

        btn_select_output_folder = QPushButton("Select Output Folder")
        btn_select_output_folder.clicked.connect(self.select_output_folder)
        layout.addWidget(btn_select_output_folder)

        btn_start_record = QPushButton("Start Recording")
        btn_start_record.clicked.connect(self.execute_record)
        layout.addWidget(btn_start_record)

        btn_generate_image = QPushButton("Generate Image")
        btn_generate_image.clicked.connect(self.execute_draw)
        layout.addWidget(btn_generate_image)

        mainTab.setLayout(layout)
        return mainTab

    def manage_recordings_tab(self):
        """Create the manage recordings page."""
        manageRecordingsTab = QWidget()
        layout = QVBoxLayout()

        btn_select_csv_file = QPushButton("Select csv-file from recording")
        btn_select_csv_file.clicked.connect(self.select_csv_file)

        layout.addWidget(btn_select_csv_file)
        manageRecordingsTab.setLayout(layout)
        return manageRecordingsTab

    def select_csv_file(self):
        csv_file, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if csv_file:
            self.file_handler.csv_file = csv_file
            logging.info("File selected %s" % (csv_file))
        else:
            logging.warn("No csv file selected!")

    def select_output_folder(self):
        output_folder = QFileDialog.getExistingDirectory(
            self, "Select Output Folder"
        )
        if output_folder:
            self.file_handler.output_path = Path(output_folder)
            logging.info("Folder selected %s" % (output_folder))
        else:
            logging.warn("No output folder selected!")

    def execute_record(self):
        record_mouse()

    def execute_draw(self):
        draw_mouse_tracks()


def start_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
