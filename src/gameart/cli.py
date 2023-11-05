import fire

from gameart.api import draw_mouse_tracks, record_mouse


def main():
    """
    Main method of the command line interface. Provides the interface to all
    public methods which can be used by the user of this python package
    """
    fire.Fire(
        {
            "record": record_mouse,
            "draw": draw_mouse_tracks,
        }
    )


if __name__ == "__main__":
    main()
