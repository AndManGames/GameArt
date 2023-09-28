import glob
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from gameart.utils import utils


def _get_latest_csv_file() -> Path:
    git_root_path = Path(utils.get_git_root_path())
    output_csv_path = git_root_path / '*.csv'

    list_of_files = glob.glob(str(output_csv_path))
    latest_file = Path(max(list_of_files, key=os.path.getctime))

    return latest_file


def draw_art():
    fig, ax = plt.subplots()

    csv_file = _get_latest_csv_file()
    data_frame_keys_pressed = pd.read_csv(csv_file)

    color_palette = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

    for index, row in data_frame_keys_pressed.iterrows():
        key = row['Key'].replace("'", "")
        duration = row['Duration']

        color = color_palette[ord(key) % len(color_palette)]

        linewidth = duration / 100.0

        ax.plot(index, 0, marker='o', markersize=10, color=color, lw=linewidth)

    ax.axis('off')

    plt.title('GameArt')
    plt.show()


if __name__ == "__main__":
    draw_art()
