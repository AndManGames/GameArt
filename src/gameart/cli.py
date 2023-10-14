import fire

from gameart.api import draw, record


def main():
    fire.Fire({"record": record, "draw": draw})


if __name__ == "__main__":
    main()
