import ctypes
import glob
import os
import subprocess
from pathlib import Path
from typing import Tuple


def _get_git_root_path() -> Path:
    """
    Gets the root path of the current git repository

    Returns:
        str: string with the root path of the current git repository
    """
    return Path(
        subprocess.Popen(
            ["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE
        )
        .communicate()[0]
        .rstrip()
        .decode("utf-8")
    )


def _get_latest_csv_file(path: Path, filter: str = "") -> Path:
    """
    Searches in given path for the csv file which was modified latest

    Args:
        path (Path): Path to folder where csv files, which should be checked,
            are stored
        filter (str): keyword which should be used to filter the csv files.
            Defaults to ''


    Raises:
        FileNotFoundError: Raises exception if no csv file exists in given path

    Returns:
        Path: Returns the path to the csv file which was modified latest. If
            filter argument is used it returns the last modified file which
            contains the keyword given
    """
    output_csv_path = path / f"*{filter}*.csv"

    list_of_files = glob.glob(str(output_csv_path))
    if len(list_of_files) > 0:
        latest_file = Path(max(list_of_files, key=os.path.getctime))
        return latest_file
    else:
        raise FileNotFoundError


def _get_screensize() -> Tuple[int, int]:
    """
    Returns the screen size as a tuple of width and height in pixels

    Returns:
        Tuple[int, int]: width, height
    """
    return ctypes.windll.user32.GetSystemMetrics(
        0
    ), ctypes.windll.user32.GetSystemMetrics(1)


def _create_output_folder(output_path: Path, folder_name: str) -> None:
    """
    Creates output folder for the given path.

    Args:
        output_path (Path): path to output directory
        folder_name (str): name of folder which shall be created
    """
    if not os.path.exists(output_path / Path(folder_name)):
        os.mkdir(output_path / Path(folder_name))
