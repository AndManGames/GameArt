from pathlib import Path

from gameart.FileHandler import FileHandlerSingleton


def test_csv_file():
    """
    Case 1: test if csv_file has been set
    """
    file_handler = FileHandlerSingleton()
    file_handler.csv_file = "data.csv"
    assert file_handler.csv_file == "data.csv"


def test_output_path():
    """
    Case 2: test if output_path has been set
    """
    file_handler = FileHandlerSingleton()
    output_path = Path("output")
    file_handler.output_path = output_path
    assert file_handler.output_path == output_path


def test_singleton_instance():
    """
    Case 3: test that there is only one instance
    """
    file_handler1 = FileHandlerSingleton()
    file_handler2 = FileHandlerSingleton()
    assert file_handler1 == file_handler2
