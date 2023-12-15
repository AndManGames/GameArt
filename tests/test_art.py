from unittest.mock import Mock, patch

import matplotlib.pyplot  # noqa: F401
import pandas

from gameart.draw import art
from gameart.utils import utils  # noqa: F401


def test_draw_mouse_tracks():
    """
    Case 1: Mock external dependencies, check if expected values are returned
    and verify that matplotlib.pyplot.show() was called to display the plot.
    """
    mock_data_frame = pandas.DataFrame(
        {
            "x-position": [1009, 1004, 1003, 1003],
            "y-position": [97, 106, 106, 107],
        }
    )
    mock_screensize = Mock(return_value=(1920, 1080))
    mock_output_folder = Mock("/mock/git/root/path/gameart_images")

    with patch("pandas.read_csv", return_value=mock_data_frame), patch(
        "gameart.utils.utils._get_screensize", mock_screensize
    ), patch(
        "gameart.utils.utils._create_output_folder", mock_output_folder
    ), patch(
        "matplotlib.pyplot.savefig"
    ) as mock_save:
        art._draw_mouse_tracks()

    assert mock_save.called
