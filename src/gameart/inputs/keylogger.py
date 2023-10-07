import datetime
import logging
import time
from typing import Any

import pandas as pd
from pynput import keyboard
from pynput.keyboard import Key, KeyCode

time_start_key_press = 0
data_frame_keys_pressed = pd.DataFrame(columns=['Key', 'Duration'])


def _on_key_press(key: Key | KeyCode | None) -> None:
    """
    This method will be called on each key press. It sets the starting timestamp of the key press to current time.time().
    The timestamp is used later to calculate the duration of each key press.

    Args:
        key (Key | KeyCode | None): This argument is the key which got pressed on the Keyboard
    """
    global time_start_key_press
    time_start_key_press = time.time()


def _on_key_release(key: Key | KeyCode | None) -> Any:
    """
    This method will be called on each key release. The duration of each key press is calculate here.
    It also writes the keylog output to a csv file and handles the termination of the key recording when the user presses 'Esc'.

    Args:
        key (Key | KeyCode | None): This argument is the key which got released on the Keyboard

    Returns:
        Any: The method returns False when the key 'Esc' was pressed or None for any other key.
    """
    global time_start_key_press, data_frame_keys_pressed

    time_taken = round(time.time() - time_start_key_press, 2)

    if key == keyboard.Key.esc:
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'keylogger_{formatted_time}.csv'

        logging.info("Recording stopped")
        logging.info(f"Log saved to {file_name}")

        data_frame_keys_pressed.to_csv(
            file_name, sep=',', encoding='utf-8')
        return False

    data_frame_keys_pressed.loc[len(data_frame_keys_pressed.index)] = [  # type: ignore
        str(key).replace("'", ""), str(time_taken)]


def _record() -> None:
    """
    Starts the listener of pynput to record keys pressed.
    """
    logging.info("Recording start")
    logging.info("Press 'Esc' to stop recording")
    logging.info("Recording...")

    with keyboard.Listener(on_press=_on_key_press, on_release=_on_key_release) as listener:
        listener.join()
