import fire

from gameart.api import (
    draw_dots,
    draw_lines,
    draw_mouse_tracks,
    record_keyboard,
    record_mouse,
)


def main():
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
