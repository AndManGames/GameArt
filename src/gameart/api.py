import logging

from pynput import keyboard

from gameart.inputs import keylogger

logging.basicConfig(level=logging.INFO)


def record() -> None:
    """
    Public function to start recording of keyboard input
    """
    logging.info("Recording start")
    logging.info("Press 'Esc' to stop recording")
    logging.info("Recording...")

    with keyboard.Listener(on_press=keylogger._on_key_press, on_release=keylogger._on_key_release) as listener:
        listener.join()
