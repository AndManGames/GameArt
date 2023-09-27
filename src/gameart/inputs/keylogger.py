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
    global time_start_key_press
    time_start_key_press = time.time()


def _on_key_release(key: Key | KeyCode | None) -> Any:
    global time_start_key_press, data_frame_keys_pressed

    time_taken = round(time.time() - time_start_key_press, 2)
    data_frame_keys_pressed.loc[len(data_frame_keys_pressed.index)] = [  # type: ignore
        str(key), str(time_taken)]

    if key == keyboard.Key.esc:
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'keylogger_{formatted_time}.csv'

        logging.info("Recording stopped")
        logging.info(f"Log saved to {file_name}")

        data_frame_keys_pressed.to_csv(
            file_name, sep='\t', encoding='utf-8')
        return False
