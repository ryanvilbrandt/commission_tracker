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
# * Finish commission confirmation
# * Order commissions by when an artist accepts them
# * Notes field for each commission? Editable on the web page
# * Can view the history of each commissions
# * Add tracking for which users have websockets open
# * Figure out way to make multiple actions in a row bog things down less. Threading of sending websockets?
# * Time counter of how long something has been in its current status
# * Change buttons to progress bar?
# * Change "User" role to "Artist" and get rid of "Is Artist"
# * Look into splitting out commission updates from websockets
