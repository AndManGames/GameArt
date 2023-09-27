import fire

from gameart.api import start_logging


def main():
    fire.Fire({
        'start_logging': start_logging
    })


if __name__ == '__main__':
    main()
