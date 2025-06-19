from argparse import ArgumentParser
from time import sleep

from src.server import Server
from src.utils import get_arg_group


def simple_run(*args, **kwargs):
    Server(*args, **kwargs)


def watchdog_run(*args, **kwargs):
    while True:
        try:
            Server(*args, **kwargs)
        except KeyboardInterrupt:
            print("To manually kill the server, send another interrupt in the next 10 seconds.")
            sleep(10)


if __name__ == '__main__':
    parser = ArgumentParser()

    server_args_group = parser.add_argument_group('server args', 'passthrough arguments to the server')
    server_args_group.add_argument('-d', '--debug', action="store_true")
    server_args_group.add_argument('-r', '--reload', action="store_true", default=None)

    parser.add_argument('-w', '--disable-watchdog', action="store_true")

    args = parser.parse_args()
    server_args = get_arg_group(parser, args, 'server args')

    if args.disable_watchdog:
        simple_run(**server_args)
    else:
        watchdog_run(**server_args)
