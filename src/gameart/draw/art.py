import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Circle

from gameart.utils import utils


def _draw_mouse_tracks(csv_file_path: str = "") -> None:
    """
    Draws a matlab figure with the recorded mouse movement displayed as a
    x-y-diagram. The movement will be drawn with lines and the mouse
    standstill positions will be drawn as circles, which vary in size
    according to the standstill duration on each position.
    The picture will be saved to the output folder.

    Args:
        csv_file_path (str): optional argument to provide csv_file_path.
        If csv_file_path is not specified, csv file will be searched in
        git root path
    """
    _, ax = plt.subplots(
        figsize=(
            utils._get_screensize()[0] / 100,
            utils._get_screensize()[1] / 100,
        )
    )
    git_root_path = utils._get_git_root_path()
    csv_file = Path(".")
    if csv_file_path == "":
        csv_file = utils._get_latest_csv_file(git_root_path, "mousetracker")
    else:
        csv_file = Path(csv_file_path)
    data_frame_mouse_movement = pd.read_csv(csv_file, index_col=0)

    x_prev, y_prev = None, None
    count_identical_rows = 0
    radius = 10
    gray_level = 0

    for _, row in data_frame_mouse_movement.iterrows():
        x, y = row["x-position"], row["y-position"]

        if x == x_prev and y == y_prev:
            count_identical_rows += 1
        else:
            if count_identical_rows >= 3:
                # Adjust the radius based on the duration of standstill
                radius = min(100, 10 + count_identical_rows)

                color = str(gray_level / 10)

                # Draw a circle with adjusted radius
                circle = Circle((x, y), radius, color=color)
                ax.add_patch(circle)

                gray_level = (gray_level + 1) % 10

            count_identical_rows = 0

        if x_prev is not None and y_prev is not None:
            # Draw a line for mouse movement
            ax.plot([x_prev, x], [y_prev, y], color="black", linewidth=0.5)

        x_prev, y_prev = x, y

    ax.set_aspect("equal", adjustable="box")
    plt.axis("off")

    output_folder_name = "gameart_images"
    utils._create_output_folder(git_root_path, output_folder_name)

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"gameart_{formatted_time}"

    try:
        plt.savefig(f"{output_folder_name}/{file_name}.png")
    except FileExistsError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
