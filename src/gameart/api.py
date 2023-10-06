import logging

from pynput import keyboard

from gameart.draw import art
from gameart.inputs import keylogger

logging.basicConfig(level=logging.INFO)


def record() -> None:
    """
    Public function to start recording of keyboard input
    """
    keylogger._record()


def draw() -> None:
    """
    Public function to draw art based on csv file input which was generated by the method 'record'
    """
    art._draw()
