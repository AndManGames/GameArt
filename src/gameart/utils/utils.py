import glob
import os
import subprocess
from pathlib import Path


def _get_git_root_path() -> Path:
    """
    Gets the root path of the current git repository

    Returns:
        str: string with the root path of the current git repository
    """
    return Path(subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8'))


def _get_latest_csv_file(path: Path) -> Path:
    """
    Searches in given path for the csv file which was modified latest

    Args:
        path (Path): Path to folder where csv files, which should be checked, are stored


    Raises:
        FileNotFoundError: Raises exception if no csv file exists in given path

    Returns:
        Path: Returns the path to the csv file which was modified latest
    """
    output_csv_path = path / '*.csv'

    list_of_files = glob.glob(str(output_csv_path))
    if len(list_of_files) > 0:
        latest_file = Path(max(list_of_files, key=os.path.getctime))
        return latest_file
    else:
        raise FileNotFoundError
