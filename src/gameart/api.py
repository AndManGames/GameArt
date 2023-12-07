import logging

logging.basicConfig(level=logging.INFO)


def record_mouse() -> None:
    """
    Public function to start recording of mouse input
    """
    try:
        import pynput  # noqa
    except ModuleNotFoundError:
        print("Try to run: pip install gameart[with-record]")

    from gameart.inputs import mousetracker

    mousetracker._record_mouse()


def draw_mouse_tracks(csv_file_path: str = "") -> None:
    """
    Public function to draw mousetracking-art based on csv file input
    which was generated by the method 'record_mouse'

    Args:
        csv_file_path (str): optional argument to provide csv_file_path.
    """
    from gameart.draw import art

    art._draw_mouse_tracks(csv_file_path)
