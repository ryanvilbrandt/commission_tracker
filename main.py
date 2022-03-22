from argparse import ArgumentParser
from time import sleep

from src.server import Server

parser = ArgumentParser()
parser.add_argument('-d', '--debug', action="store_true")
parser.add_argument('-w', '--disable-watchdog', action="store_true")
args = parser.parse_args()

while True:
    try:
        Server(debug=args.debug)
    except KeyboardInterrupt:
        if args.disable_watchdog:
            break
        print("To manually kill the server, send another interrupt in the next 10 seconds.")
        sleep(10)

# TODO:
# * Add tracking for which users have websockets open
# * Change buttons to progress bar?
# * Group "assigned to others" commissions by artist
# * Editable text fields
# * Make newlines work in commission text fields somehow
# * Figure out way to make multiple actions in a row bog things down less. Threading of sending websockets?
# * Allow upload/drag-and-drop of finished images onto commissions
