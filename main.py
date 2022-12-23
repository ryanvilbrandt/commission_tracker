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
# * Fix unicode in notes
# * Add email field to commissions and an "Update Email" button for quick updates of the data
# * Add "Update name" button to commissions
# * Add Archive button
# * Add undo Archive/Email/Refund buttons.
# * Add Export Images option. Group images by commissioner name/email
# * Add sorting options for the user:
#   * Updated TS
#   * Email
#   * Username
#   * Created TS
#   * Commission ID
# * Add ability to visually group commissions together by user
# * Look into hooking Queue Open/Close to the Twitch Overlay
# * Add tracking for which users have websockets open
# * Figure out way to make multiple actions in a row bog things down less.
#   * I think bottle is single-threaded, so may not be able to manage multiple threads.
#   * Switch to pushing updates over the websocket itself? Could be single-threaded that way.
#   * Figure out if bottle can be multi-threaded. If so, create threading.lock when writing.
