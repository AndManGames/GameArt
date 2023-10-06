import matplotlib.pyplot as plt
import pandas as pd

from gameart.utils import utils


def _draw():
    """
    Draws an matplotlib diagram based on a csv input files which needs to have the columns Key (string) and Duration(float)
    """
    fig, ax = plt.subplots()

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
