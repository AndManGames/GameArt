from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw

from gameart.utils import utils


def _map_duration_to_color(duration: float) -> Tuple[int, int, int]:
    color_ranges = {
        (0.0, 0.1): (255, 0, 0),     # Red
        (0.1, 0.2): (0, 255, 0),     # Green
        (0.2, 0.3): (0, 0, 255),     # Blue
        (0.3, 0.4): (255, 255, 0),   # Yellow
        (0.4, 0.5): (0, 255, 255)    # Cyan
    }
    
    for (min_val, max_val), color in color_ranges.items():
        if min_val <= duration < max_val:
            return color
    return (0, 0, 0)  # Default color for unmatched values


def _draw_dots() -> None:
    """
    Draws an matplotlib diagram based on a csv input files which needs to have the columns Key (string) and Duration(float)
    """
    _, ax = plt.subplots()

    git_root_path = utils._get_git_root_path()
    csv_file = utils._get_latest_csv_file(git_root_path)
    data_frame_keys_pressed = pd.read_csv(csv_file)

    color_palette = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

    for index, row in data_frame_keys_pressed.iterrows():
        key = row['Key']
        duration = row['Duration']

        color = color_palette[ord(key) % len(color_palette)]

        linewidth = duration / 100.0

        ax.plot(index, 0, marker='o', markersize=10, color=color, lw=linewidth)

    ax.axis('off')

    plt.title('GameArt')
    plt.show()


def _draw_lines() -> None:
    canvas_size = 400
    canvas = Image.new('RGB', (canvas_size, canvas_size), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    x, y = canvas_size // 2, canvas_size // 2
    speed = 15
    current_thickness = 10

    git_root_path = utils._get_git_root_path()
    csv_file = utils._get_latest_csv_file(git_root_path)
    data_frame_keys_pressed = pd.read_csv(csv_file)

    directions = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}

    for _, row in data_frame_keys_pressed.iterrows():
        key = row['Key']
        duration = round(float(row['Duration']), 2)
        
        if key in directions:
            dx, dy = directions[key]
            x_new, y_new = x + dx * speed, y + dy * speed
            
            x_new = max(0, min(x_new, canvas_size - 1))
            y_new = max(0, min(y_new, canvas_size - 1))
            
            current_color = _map_duration_to_color(duration)
            
            draw.line([(x, y), (x_new, y_new)], fill=current_color, width=current_thickness)
            
            x, y = x_new, y_new
        else:
            pass

    canvas.show()
