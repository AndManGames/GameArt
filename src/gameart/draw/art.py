import logging
import platform
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Circle

from gameart.FileHandler import FileHandlerSingleton
from gameart.utils import utils

logging.basicConfig(level=logging.INFO)


def _draw_mouse_tracks() -> None:
    """
    Draws a matlab figure with the recorded mouse movement displayed as a
    x-y-diagram. The movement will be drawn with lines and the mouse
    standstill positions will be drawn as circles, which vary in size
    according to the standstill duration on each position.
    The picture will be saved to the output folder.
    """
    file_handler = FileHandlerSingleton()
    csv_file = Path(file_handler.csv_file)
    csv_file_name = csv_file.stem
    output_path = file_handler.output_path
    total_path = output_path / csv_file

    logging.info("Read csv file...")
    data_frame_mouse_movement = pd.read_csv(total_path, index_col=0)

    if platform.system() == "Windows":
        _, ax = plt.subplots(
            figsize=(
                utils._get_screensize()[0] / 100,
                utils._get_screensize()[1] / 100,
            )
        )
    else:
        screensize_default = (1920 / 100, 1080 / 100)
        _, ax = plt.subplots(figsize=screensize_default)

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
    utils._create_output_folder(output_path, output_folder_name)

    file_name = f"gameart_{csv_file_name}"

    try:
        plt.savefig(f"{output_path}/{output_folder_name}/{file_name}.png")
        logging.info(
            "Saved to %s/%s/%s.png"
            % (output_path, output_folder_name, file_name)
        )
    except FileExistsError as e:
        logging.error("Error: %s - %s." % (e.filename, e.strerror))
