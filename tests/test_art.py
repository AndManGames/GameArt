from unittest.mock import patch

import matplotlib.pyplot
import pandas

from gameart.draw import art
from gameart.utils import utils


def test_draw_dots():
    """
    Case 1: Mock external dependencies, check if expected values are returned and
    verify that matplotlib.pyplot.show() was called to display the plot.
    """
    mock_git_root_path = "/mock/git/root/path"
    mock_csv_file = "/mock/csv/file.csv"
    mock_data_frame = pandas.DataFrame(
        {'Key': ['A', 'B', 'C'], 'Duration': [50.0, 75.0, 100.0]})

    with patch('gameart.utils.utils._get_git_root_path', return_value=mock_git_root_path), \
            patch('gameart.utils.utils._get_latest_csv_file', return_value=mock_csv_file), \
            patch('pandas.read_csv', return_value=mock_data_frame), \
            patch('matplotlib.pyplot.show') as mock_show:

        art._draw_dots()

    assert mock_show.called
