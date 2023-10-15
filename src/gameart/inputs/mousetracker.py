import ctypes
import datetime
import logging
from typing import Any

import pandas as pd
from pynput import mouse

from gameart.utils import utils

# Ensuring consistent coordinates between listener and controller on Windows
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)


data_frame_mouse_movement = pd.DataFrame(columns=["x-position", "y-position"])


def _on_move(x: float, y: float) -> None:
    """
    Method is called when mouse is moved. Saves the coordinates of each mouse
    position to a pandas dataframe.

    Args:
        x (float): x-coordinate of the current mouse position
        y (float): y-coordinate of the current mouse position
    """
    global data_frame_mouse_movement

    y = abs(
        y - utils._get_screensize()[1]
    )  # flip y value, so that bottom of monitor is 0
    logging.info("Pointer moved to {0}".format((x, y)))

    data_frame_mouse_movement.loc[
        len(data_frame_mouse_movement.index)
    ] = [  # type: ignore
        x,
        y,
    ]


def _on_click(x: float, y: float, button: mouse.Button, pressed: bool) -> Any:
    """
    Method is called when a mouse button is clicked. Stops recording on
    right mouse button click.

    Args:
        x (float): x-coordinate of the current mouse position
        y (float): y-coordinate of the current mouse position
        button (mouse.Button): mouse button which was clicked
        pressed (bool): is mouse button currently pressed?

    Returns:
        Any: returns False when right mouse button was clicked,
            for all other cases method returns None
    """
    global data_frame_mouse_movement

    logging.info(
        "{0} at {1}".format("Pressed" if pressed else "Released", (x, y))
    )
    if pressed and button == mouse.Button.right:
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"mousetracker_{formatted_time}.csv"

        logging.info("Recording stopped")
        logging.info(f"Log saved to {file_name}")

        data_frame_mouse_movement.to_csv(file_name, sep=",", encoding="utf-8")

        return False


def _record() -> None:
    """
    Starts the listener of pynput to record mouse movement and buttons.
    """
    logging.info("Recording started")
    logging.info("Press Right Mouse Button to stop recording")
    logging.info("Recording...")

    with mouse.Listener(on_move=_on_move, on_click=_on_click) as listener:
        try:
            listener.join()
        except KeyError as e:
            logging.error("{0} was clicked".format(e.args[0]))
