from unittest.mock import patch

import pytest
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QApplication

from gameart.gui import MainWindow


@pytest.fixture(scope="session")
def app(request):
    """
    Fixture to create a QApplication instance for testing.
    """
    app = QApplication([])
    yield app
    app.quit()


def test_base_folder(app):
    """
    Test that the base folder can be set and retrieved.
    """
    window = MainWindow()
    window.base_folder = "test_folder"
    assert window.base_folder == "test_folder"


def test_select_output_folder(app):
    """
    Test that the output folder can be selected.
    """
    window = MainWindow()
    with patch(
        "gameart.gui.QFileDialog.getExistingDirectory", return_value="/output"
    ):
        window._select_output_folder()
        assert str(window.file_handler.output_path.resolve()) == "C:\\output"


def test_select_output_folder_cancelled(app):
    """
    Test that the output folder can be cancelled.
    """
    window = MainWindow()
    with patch(
        "gameart.gui.QFileDialog.getExistingDirectory", return_value=""
    ):
        window._select_output_folder()
        assert (
            str(window.file_handler.output_path.resolve()) == "C:\\output"
        )  # same as before, then no new output folder has been set


def test_update_list_view(app):
    """
    Test that the list view can be updated.
    """
    window = MainWindow()
    window.base_folder = "test_folder"
    window._update_list_view("test_folder")
    assert window.list_view.rootIndex().data() == "test_folder"


def test_on_list_view_clicked_csv(app):
    """
    Test that the file handler is updated when a CSV file is clicked.
    """
    window = MainWindow()
    index = QModelIndex()
    index.data = lambda _: "test.csv"
    window.file_model.fileInfo = lambda _: index
    window._on_list_view_clicked(index)
    assert window.file_handler.csv_file == "test.csv"


def test_on_list_view_clicked_not_csv(app):
    """
    Test that the file handler is not updated when a non-CSV file is clicked.
    """
    window = MainWindow()
    index = QModelIndex()
    index.data = lambda _: "test.txt"
    window.file_model.fileInfo = lambda _: index
    window._on_list_view_clicked(index)
    assert window.file_handler.csv_file is None


def test_select_base_folder(app):
    """
    Test that the base folder can be selected.
    """
    window = MainWindow()
    with patch(
        "gameart.gui.QFileDialog.getExistingDirectory", return_value="/folder"
    ):
        window._select_base_folder()
        assert window.base_folder == "/folder"


def test_select_base_folder_cancelled(app):
    """
    Test that the base folder can be cancelled.
    """
    window = MainWindow()
    with patch(
        "gameart.gui.QFileDialog.getExistingDirectory", return_value=""
    ):
        window._select_base_folder()
        assert window.base_folder == ""


def test_execute_record(app):
    """
    Test that the record mouse method is called.
    """
    window = MainWindow()
    with patch("gameart.gui.record_mouse") as mock_record_mouse:
        window._execute_record()
        mock_record_mouse.assert_called()


def test_execute_draw(app):
    """
    Test that the draw mouse tracks method is called.
    """
    window = MainWindow()
    with patch("gameart.gui.draw_mouse_tracks") as mock_draw_mouse_tracks:
        window._execute_draw()
        mock_draw_mouse_tracks.assert_called()
