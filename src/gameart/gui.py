import importlib.metadata
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
)

from gameart.api import draw_mouse_tracks, record_mouse
from gameart.utils import utils

screen_width = utils._get_screensize()[0]
screen_height = utils._get_screensize()[1]
window_width = screen_width // 5
window_height = screen_height // 3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            f"GameArt - {importlib.metadata.version('gameart')}"
        )
        self.setGeometry(
            screen_width // 2 - window_width // 2,
            screen_height // 2 - window_height // 2,
            window_width,
            window_height,
        )

        # Create buttons
        self.select_csv_btn = QPushButton("Select CSV file", self)
        self.select_csv_btn.clicked.connect(self.select_csv)
        self.select_output_folder_btn = QPushButton(
            "Select Output Folder", self
        )
        self.select_output_folder_btn.clicked.connect(
            self.select_output_folder
        )
        self.record_btn = QPushButton("Start Recording", self)
        self.record_btn.clicked.connect(self.execute_record)
        self.draw_btn = QPushButton("Draw", self)
        self.draw_btn.clicked.connect(self.execute_draw)
        self.draw_btn.setEnabled(False)

        # Create labels
        self.subtitle_label = QLabel(
            f"{importlib.metadata.metadata('gameart')['summary']}", self
        )
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setMinimumHeight(50)
        self.csv_label = QLabel("", self)
        self.csv_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.csv_label.setMinimumHeight(50)
        self.output_folder_label = QLabel("", self)
        self.output_folder_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.output_folder_label.setMinimumHeight(50)

        # Set position and size
        self.subtitle_label.setGeometry(10, 10, window_width, 50)
        self.record_btn.setGeometry(window_width // 2 - 100, 50, 200, 50)
        self.select_csv_btn.setGeometry(window_width // 2 - 100, 120, 200, 50)
        self.csv_label.setGeometry(275, 120, 500, 50)
        self.select_output_folder_btn.setGeometry(
            window_width // 2 - 100, 190, 200, 50
        )
        self.output_folder_label.setGeometry(275, 190, 500, 50)
        self.draw_btn.setGeometry(window_width // 2 - 100, 260, 200, 50)

        # Path variables
        self.csv_path = ""
        self.output_folder_path = ""

    def select_csv(self):
        csv_file, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if csv_file:
            self.csv_path = csv_file
            self.csv_label.setText(f"{csv_file}")
            self.check_paths()

    def select_output_folder(self):
        output_folder = QFileDialog.getExistingDirectory(
            self, "Select Output Folder"
        )

        if output_folder:
            self.output_folder_path = output_folder
            self.output_folder_label.setText(f"{output_folder}")
            self.check_paths()

    def check_paths(self):
        if self.csv_path and self.output_folder_path:
            self.draw_btn.setEnabled(True)
        else:
            self.draw_btn.setEnabled(False)

    def execute_record(self):
        record_mouse()

    def execute_draw(self):
        draw_mouse_tracks(self.csv_path, self.output_folder_path)


def start_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
