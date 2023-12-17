import logging
import shutil
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest

from gameart.utils import utils


@pytest.fixture
def temp_directory(tmp_path: Path) -> Generator[Path, Any, Any]:
    """
    Creates a temporary directory for testing. And deletes it afterwards.

    Args:
        tmp_path (Path): Path to temporary directory where csv files should be
        stored to

    Yields:
        Path: Generator[Path, Any, Any]
    """
    temp_dir = tmp_path / "csv_test_dir"
    temp_dir.mkdir()
    yield temp_dir

    try:
        shutil.rmtree(temp_dir)
    except OSError as e:
        logging.error("Error: %s - %s." % (e.filename, e.strerror))


def test_get_latest_csv_file_no_files(temp_directory: Path) -> None:
    """
    Case 1: Test when no CSV files exist in the directory.

    Args:
        temp_directory (Path): Path to temporary directory where csv files are
        stored
    """
    with pytest.raises(FileNotFoundError):
        utils._get_latest_csv_file(temp_directory)


def test_get_latest_csv_file_single_file(temp_directory: Path) -> None:
    """
    Case 2: Create a single CSV file in the directory.

    Args:
        temp_directory (Path): Path to temporary directory where csv files are
        stored
    """
    csv_file = temp_directory / "test.csv"
    csv_file.touch()

    latest_file = utils._get_latest_csv_file(temp_directory)
    assert latest_file == csv_file


def test_get_latest_csv_file_multiple_files(temp_directory: Path) -> None:
    """
    Case 3: Create multiple CSV files with different modification times.

    Args:
        temp_directory (Path): Path to temporary directory where csv files are
        stored
    """
    csv_file1 = temp_directory / "file1.csv"
    csv_file1.touch()

    csv_file2 = temp_directory / "file2.csv"
    csv_file2.touch()

    # Sleep briefly to ensure file2 has a later modification time.
    import time

    time.sleep(0.1)

    csv_file3 = temp_directory / "file3.csv"
    csv_file3.touch()

    latest_file = utils._get_latest_csv_file(temp_directory)
    assert latest_file == csv_file3


def test_get_latest_csv_file_with_filter(
    temp_directory: Path,
) -> None:
    """
    Case 4: Create two CSV file in the directory. One with and one without a
    keyword. Checks if the file with the given filter argument is selected.

    Args:
        temp_directory (Path): Path to temporary directory where csv files are
        stored
    """
    csv_file1 = temp_directory / "test.csv"
    csv_file1.touch()

    csv_file2 = temp_directory / "test_keyword.csv"
    csv_file2.touch()

    latest_file = utils._get_latest_csv_file(temp_directory, "keyword")
    assert latest_file == csv_file2
