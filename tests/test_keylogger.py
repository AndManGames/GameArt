import os
import time

import pandas as pd
from pynput.keyboard import Key, KeyCode

from gameart.inputs import keylogger
from gameart.utils import utils


def test_key_press_and_release_duration_zero():
    """
    Case 1: Simulate key presses and releases of one Key with 0s duration.
        Output csv should only contain 1 row with the values 'Key' and
        'Duration' of the Key
    """
    keylogger._on_key_press(KeyCode(char="A"))
    keylogger._on_key_release(KeyCode(char="A"))

    keylogger._on_key_release(Key.esc)

    git_root_path = utils._get_git_root_path()
    csv_file = utils._get_latest_csv_file(git_root_path)
    data_frame_keys_pressed = pd.read_csv(csv_file)

    assert data_frame_keys_pressed["Key"].iloc[0] == "A"
    assert data_frame_keys_pressed["Duration"].iloc[0] == 0
    assert len(data_frame_keys_pressed.index) == 1

    if os.path.isfile(csv_file):
        os.remove(csv_file)
    else:
        raise FileNotFoundError


def test_key_press_and_release_duration_one():
    """
    Case 2: Simulate key presses and releases of one Key with 1s duration.
        Output csv should only contain 2 rows with the values 'Key' and
        'Duration' the previous test and this one
    """
    keylogger._on_key_press(KeyCode(char="B"))
    time.sleep(1.0)
    keylogger._on_key_release(KeyCode(char="B"))

    keylogger._on_key_release(Key.esc)

    git_root_path = utils._get_git_root_path()
    csv_file = utils._get_latest_csv_file(git_root_path)
    data_frame_keys_pressed = pd.read_csv(csv_file)

    assert data_frame_keys_pressed["Key"].iloc[0] == "A"
    assert data_frame_keys_pressed["Duration"].iloc[0] == 0
    assert data_frame_keys_pressed["Key"].iloc[1] == "B"
    assert data_frame_keys_pressed["Duration"].iloc[1] >= 1.0
    assert len(data_frame_keys_pressed.index) == 2

    if os.path.isfile(csv_file):
        os.remove(csv_file)
    else:
        raise FileNotFoundError


def test_one_successful_and_one_unsuccessful_key_press():
    """
    Case 3: Simulate key presses and releases of one Key and simulate only a
    key press without a release of another Key. Output csv should only contain
    3 rows with the values 'Key' and 'Duration' the previous tests and this one
    """
    keylogger._on_key_press(KeyCode(char="C"))
    keylogger._on_key_release(KeyCode(char="C"))
    keylogger._on_key_press(KeyCode(char="D"))

    keylogger._on_key_release(Key.esc)

    git_root_path = utils._get_git_root_path()
    csv_file = utils._get_latest_csv_file(git_root_path)
    data_frame_keys_pressed = pd.read_csv(csv_file)

    assert data_frame_keys_pressed["Key"].iloc[0] == "A"
    assert data_frame_keys_pressed["Duration"].iloc[0] == 0
    assert data_frame_keys_pressed["Key"].iloc[1] == "B"
    assert data_frame_keys_pressed["Duration"].iloc[1] >= 1.0
    assert data_frame_keys_pressed["Key"].iloc[2] == "C"
    assert data_frame_keys_pressed["Duration"].iloc[2] == 0
    assert len(data_frame_keys_pressed.index) == 3

    if os.path.isfile(csv_file):
        os.remove(csv_file)
    else:
        raise FileNotFoundError
