import ctypes
import datetime
import logging
import threading
import time
from typing import Any

import pandas as pd
from pynput import mouse

from gameart.FileHandler import FileHandlerSingleton
from gameart.utils import utils

# Ensuring consistent coordinates between listener and controller on Windows
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

data_frame_mouse_movement = pd.DataFrame(columns=["x-position", "y-position"])
data_frame_mutex = threading.Lock()

record_thread = None
exit_event = threading.Event()


def _record_positions(fps: int) -> None:
    """
    Saves the coordinates of the current mouse position every 1/fps seconds to
    a pandas dataframe.

    Args:
        fps (int): how many times per second should the mouse position be
        saved to the pandas data_frame
    """
    global data_frame_mouse_movement
    while not exit_event.is_set():
        with data_frame_mutex:
            mouse_position = mouse.Controller().position
            x, y = mouse_position[0], mouse_position[1]

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

        time.sleep(1 / fps)


def _on_click(
    x: float, y: float, button: mouse.Button, pressed: bool, **kwargs
) -> Any:
    """
    Method is called when a mouse button is clicked. Stops recording on
    right mouse button click.
    Therefore it sets the exit event for the record_thread.

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
        logging.info("Recording stopped")

        exit_event.set()

        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"mousetracker_{formatted_time}.csv"

        file_handler = FileHandlerSingleton()
        output_path = file_handler.output_path
        file_handler.csv_file = file_name
        total_path = output_path / file_name

        data_frame_mouse_movement.to_csv(total_path, sep=",", encoding="utf-8")

        logging.info("Log saved to %s" % (total_path))

        return False


def _record_mouse() -> None:
    """
    Starts the listener of pynput to record mouse movement and buttons.
    Uses threading to both detect pynput listener and controller at the same
    time.
    """
    logging.info("Recording started")
    logging.info("Press Right Mouse Button to stop recording")
    logging.info("Recording...")

    listener = mouse.Listener(on_click=_on_click)
    listener.start()

    global record_thread
    record_thread = threading.Thread(target=_record_positions(30))
    record_thread.daemon = True
    record_thread.start()
