import logging
import os
import re
import sys
from configparser import RawConfigParser
from logging.handlers import TimedRotatingFileHandler
from shutil import copyfile
from typing import List, Tuple

import gevent
from geventwebsocket import WebSocketError

websocket_list = []


# Taken from http://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/
class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


def setup_logging(name, log_level=None, capture_stderr=False):
    cfg = load_config()
    level = getattr(logging, cfg.get('Logging', 'level') if log_level is None else log_level)
    logs_folder = './logs'
    os.makedirs(logs_folder, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = TimedRotatingFileHandler(os.path.join(logs_folder, name + ".log"), when="midnight")
    formatter = logging.Formatter(cfg.get('Logging', 'format'), cfg.get('Logging', 'date format'))
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if capture_stderr:
        stderr_logger = logging.getLogger('STDERR')
        stderr_logger.addHandler(handler)
        sl = StreamToLogger(stderr_logger, logging.ERROR)
        sys.stderr = sl

    return logger


def get_config_path():
    return os.path.join("conf", "config.ini")


def load_config() -> RawConfigParser:
    config_path = get_config_path()
    # Check for config file. If it doesn't exist, copy it over
    if not os.path.isfile(config_path):
        dist_config_path = os.path.join("conf", "config.ini.dist")
        copyfile(dist_config_path, config_path)
    # Load config file and return it
    cfg = RawConfigParser()
    cfg.read(config_path)
    return cfg


def ordinal(num: str):
    if not num.isdigit():
        return num.title()
    suffix = {"1": "st", "2": "nd", "3": "rd"}
    return num + suffix.get(num, "th") + " Level"


def str_to_bool(s):
    return s and str(s).lower()[0] in ["t", "1", "y"]


def websocket_loop(ws):
    # TODO Figure out why this stops processing of the main loop when sleep() is called
    global websocket_list
    print("Opening Websocket {}".format(ws), flush=True)
    websocket_list.append(ws)
    try:
        while True:
            # Checking if websocket has been closed by the client
            with gevent.Timeout(1.0, False):
                ws.receive()
            if ws.closed:
                print("WebSocket was closed by the client: {}".format(ws), flush=True)
                break
    except Exception as e:
        print("Error in WebSocket loop: {}".format(e), flush=True)
    finally:
        if not ws.closed:
            print("Closing WebSocket: {}".format(ws), flush=True)
            ws.close()
        try:
            websocket_list.remove(ws)
        except ValueError as e:
            print(e, ws)


def send_to_websockets(payload):
    global websocket_list
    print(websocket_list, flush=True)
    for ws in websocket_list[:]:
        try:
            print(f"Sending payload to {ws}", flush=True)
            ws.send(payload)
        except WebSocketError:
            print(f"Failed to send message to {ws}. Removing from list", flush=True)
            websocket_list.remove(ws)
        except Exception as e:
            print(f"Error when sending message to {ws}. {e}", flush=True)
            websocket_list.remove(ws)


def add_hrefs_to_string(s: str) -> str:
    return re.sub(r"(https?://[^\s'\",]+)", r'<a href="\1">\1</a>', s)


def link_images(s: str) -> List[str]:
    return [f'<a href="{image}">' for image in s.split(", ")]


def get_status(commission: dict) -> Tuple[str, str]:
    if commission["invoiced"] and not commission["paid"]:
        return "invoiced", f"Emailed"
    elif commission["finished"]:
        if not commission["invoiced"]:
            return "finished_not_emailed", r"Not Emailed"
        else:
            return "finished", r"Finished! \o/"
    elif commission["paid"]:
        return "paid", f"Paid"
    elif commission["accepted"]:
        return "accepted", f"Accepted"
    elif commission["assigned_to"] != -1:
        return "not_accepted", f"Not yet accepted"
    elif commission["allow_any_artist"]:
        return "claimable", "Claimable by Anyone"
    else:
        return "exclusive", f"Exclusive Request for {commission['artist_choice']}"