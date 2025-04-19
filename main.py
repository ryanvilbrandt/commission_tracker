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

# TODO:
# * Commissions in the process of having their image uploaded shouldn't be replaced on websocket push.
# * "Mark as Finished" and "Change Image" buttons instead of text after an image has been dragged to the box
# * Add email field to commissions and an "Update Email" button for quick updates of the data
# * Add "Update name" button to commissions
# * Add Archive button
# * Add undo Archive/Email/Refund buttons.
# * Fix unicode in notes
# * Add Export Images option. Group images by commissioner name/email
# * Add sorting options for the user:
#   * Updated TS
#   * Email
#   * Username
#   * Created TS
#   * Commission ID
# * Add ability to visually group commissions together by user
# * Add "unclick" admin buttons for emailed and refunded
# * Look into hooking Queue Open/Close to the Twitch Overlay
# * Add tracking for which users have websockets open
# * Figure out way to make multiple actions in a row bog things down less.
#   * I think bottle is single-threaded, so may not be able to manage multiple threads.
#   * Switch to pushing updates over the websocket itself? Could be single-threaded that way.
#   * Figure out if bottle can be multi-threaded. If so, create threading.lock when writing.
