import bottle
from bottle_websocket import GeventWebSocketServer
from fasteners import process_lock

from src.endpoints import init, load_wsgi_endpoints
from src.utils import load_config

VERSION = (0, 0, 1)


class Server:
    """
    On load:
     - Check if any other server instances are running, fail if so.
     - Establish logging to the server.log file. Redirect stderr to this log file, to catch the output thrown
       by the Bottle server.
     - Load the WSGI functions.
     - Start the Bottle server.
    """

    server_thread = None
    interval = None

    def __init__(self, host=None, port=None, run_as_thread=None, reload=None, debug=False):
        self._get_process_lock()

        cfg = load_config()
        # Send stderr to logs if we're not running in debug mode
        # self.logger = setup_logging("log", log_level=log_level, capture_stderr=not debug)

        # Load global DB connection
        # connect_to_db()

        # Load WSGI endpoints
        bottle.TEMPLATES.clear()
        bottle.debug(debug)
        self.app = bottle.Bottle()
        init(cfg)
        load_wsgi_endpoints(self.app)

        if debug:
            print("\nLoaded routes:")
            for r in self.app.routes:
                print(r)
            print("")

        self._init_server(
            host=cfg.get("Settings", "host") if host is None else host,
            port=cfg.getint("Settings", "port") if port is None else port,
            run_as_thread=cfg.getboolean("Settings", "run as thread") if run_as_thread is None else run_as_thread,
			reload=cfg.get("Settings", "reload") if reload is None else reload
        )

    @staticmethod
    def _get_process_lock():
        lock = process_lock.InterProcessLock("server.lock")
        if not lock.acquire(blocking=False):
            raise ChildProcessError("Server process is already running")

    def _init_server(self, host=None, port=None, run_as_thread=False, reload=False):
        if run_as_thread:
            from threading import Thread
            self.server_thread = Thread(name="CommissionServer", target=self._run_server, args=[host, port, reload],
                                        daemon=True)
            self.server_thread.start()
            print("Server thread started.")
        else:
            self._run_server(host, port, reload)

    def _run_server(self, host, port, reload):
        self.app.run(host=host, port=port, reloader=reload, server=GeventWebSocketServer)
        print("Server instance is ending.")


if __name__ == "__main__":
    Server()
