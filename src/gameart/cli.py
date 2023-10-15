import fire

from gameart.api import (
    draw_dots,
    draw_lines,
    draw_mouse_tracks,
    record_keyboard,
    record_mouse,
)


def main():
    """
    Main method of the command line interface. Provides the interface to all
    public methods which can be used by the user of this python package
    """
    fire.Fire(
        {
            "record_keyboard": record_keyboard,
            "record_mouse": record_mouse,
            "draw_dots": draw_dots,
            "draw_lines": draw_lines,
            "draw_mouse_tracks": draw_mouse_tracks,
        }
    )


if __name__ == "__main__":
    main()
