from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Circle
from PIL import Image, ImageDraw

from gameart.utils import utils


def _map_duration_to_color(
    duration: float, df: pd.DataFrame
) -> Tuple[int, int, int]:
    """
    Method to map the Duration of a key press to a color

    Args:
        duration (float): Duration from key press which was recorded
        df (pd.DataFrame): Dataframe which was parsed from the keylogger

    Returns:
        Tuple[int, int, int]: Tuple of the three colors red, green and blue
            which where mapped based on the key press duration
    """
    colormap = plt.get_cmap("viridis")
    normalized_duration = (duration - df["Duration"].min()) / (
        df["Duration"].max() - df["Duration"].min()
    )
    rgba_color = colormap(normalized_duration)
    red = int(255 * rgba_color[0])
    green = int(255 * rgba_color[1])
    blue = int(255 * rgba_color[2])

    return (red, green, blue)


def _draw_dots() -> None:
    """
    Draws an matplotlib diagram based on a csv input files which needs to have
    the columns Key (string) and Duration(float)
    """
    _, ax = plt.subplots()

    git_root_path = utils._get_git_root_path()
    csv_file = utils._get_latest_csv_file(git_root_path, "keylogger")
    data_frame_keys_pressed = pd.read_csv(csv_file)

    color_palette = ["red", "blue", "green", "yellow", "purple", "orange"]

    for index, row in data_frame_keys_pressed.iterrows():
        key = row["Key"]
        duration = row["Duration"]

        color = color_palette[ord(key) % len(color_palette)]

        linewidth = duration / 100.0

        ax.plot(index, 0, marker="o", markersize=10, color=color, lw=linewidth)

    ax.axis("off")

    plt.title("GameArt")
    plt.show()


def _draw_lines() -> None:
    """
    Draws a figure with PIL where the track of the line is based on WASD input
    from the keyboard recording
    """
    canvas_size = 400
    canvas = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    x, y = canvas_size // 2, canvas_size // 2
    speed = 15
    current_thickness = 5

    git_root_path = utils._get_git_root_path()
    csv_file = utils._get_latest_csv_file(git_root_path, "keylogger")
    data_frame_keys_pressed = pd.read_csv(csv_file)

    directions = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}

    for _, row in data_frame_keys_pressed.iterrows():
        key = row["Key"]
        duration = round(float(row["Duration"]), 2)
        if key in directions:
            dx, dy = directions[key]
            x_new, y_new = x + dx * speed, y + dy * speed
            x_new = max(0, min(x_new, canvas_size - 1))
            y_new = max(0, min(y_new, canvas_size - 1))
            current_color = _map_duration_to_color(
                duration, data_frame_keys_pressed
            )
            draw.line(
                [(x, y), (x_new, y_new)],
                fill=current_color,
                width=current_thickness,
            )
            x, y = x_new, y_new
        else:
            pass

    canvas.show()


def _draw_mouse_tracks() -> None:
    """
    Draws a matlab figure with the recorded mouse movement displayed as a
    x-y-diagram. The movement will be drawn with lines and the mouse
    standstill positions will be drawn as circles, which vary in size
    according to the standstill duration on each position
    """
    _, ax = plt.subplots(
        figsize=(
            utils._get_screensize()[0] / 100,
            utils._get_screensize()[1] / 100,
        )
    )

    git_root_path = utils._get_git_root_path()
    csv_file = utils._get_latest_csv_file(git_root_path, "mousetracker")
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
                radius = 10 + count_identical_rows

                color = str(gray_level / 5)

                # Draw a circle with adjusted radius
                circle = Circle((x, y), radius, color=color)
                ax.add_patch(circle)

                gray_level = (gray_level + 1) % 5

            count_identical_rows = 0

        if x_prev is not None and y_prev is not None:
            # Draw a line for mouse movement
            ax.plot([x_prev, x], [y_prev, y], color="black", linewidth=1)

        x_prev, y_prev = x, y

    plt.axis("off")
    plt.show()
