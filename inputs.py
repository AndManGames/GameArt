import os
import time
from typing import Any

import pandas as pd
import pynput
from pynput import keyboard
from pynput.keyboard import Key, KeyCode

time_start_key_press = 0
data_frame_keys_pressed = pd.DataFrame(columns=['Key', 'Duration'])


def on_key_press(key: Key | KeyCode | None) -> None:
    global time_start_key_press
    time_start_key_press = time.time()


def on_key_release(key: Key | KeyCode | None) -> Any:
    global time_start_key_press, data_frame_keys_pressed

    time_taken = round(time.time() - time_start_key_press, 2)
    data_frame_keys_pressed.loc[-1] = [  # type: ignore
        str(key), str(time_taken)]
    data_frame_keys_pressed.index = data_frame_keys_pressed.index + 1

    if key == keyboard.Key.esc:
        data_frame_keys_pressed.to_csv(
            'keylogger.csv', sep='\t', encoding='utf-8')
        return False


if __name__ == "__main__":
    if os.path.exists("keylogger.csv"):
        os.remove("keylogger.csv")

    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()
