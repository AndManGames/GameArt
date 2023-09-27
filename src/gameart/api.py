import os

from pynput import keyboard

from gameart.inputs import keylogger


def start_logging() -> None:
    if os.path.exists("keylogger.csv"):
        os.remove("keylogger.csv")

    with keyboard.Listener(on_press=keylogger._on_key_press, on_release=keylogger._on_key_release) as listener:
        listener.join()
