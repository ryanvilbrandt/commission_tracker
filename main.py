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
# * Totals on every queue
# * Try click-uploading commissions and see why it breaks
# * Notes field for each commission? Editable on the web page
# * Can view the history of each commissions
# * Add tracking for which users have websockets open
# * Figure out way to make multiple actions in a row bog things down less. Threading of sending websockets?
# * Change buttons to progress bar?
# * Look into splitting out commission updates from websockets
# * Look into hooking Queue Open/Close to the Twitch Overlay
