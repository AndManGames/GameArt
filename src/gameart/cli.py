import fire

from gameart.api import record


def main():
    fire.Fire({
        'record': record
    })


if __name__ == '__main__':
    main()
