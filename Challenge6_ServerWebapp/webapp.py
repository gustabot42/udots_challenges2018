#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Webapp and web socket for registed sum server
"""

# Standard Libraries
import logging
import os.path
# Thirdparty Libraries
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpclient import TCPClient
from tornado.options import define, options
from tornado import web
import tornado.websocket


# Configuration
define("web_port", default=8899, help="Webapp run on the given port", type=int)
define("listen_host", default='localhost', help="Listen to the given host", type=int)
define("listen_port", default=27878, help="Listen on the given port", type=int)
logger = logging.getLogger(__name__)


class Application(web.Application):
    def __init__(self):
        handlers = [
            (r'/', web.RedirectHandler, {"url": "/static/index.html"}),
            (r"/socket", SocketHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


class SocketHandler(tornado.websocket.WebSocketHandler):
    """
    Web socket for registed data from sum server
    """
    # set of client waiting for message
    waiters = set()

    def open(self):
        # add clients to waiting set
        SocketHandler.waiters.add(self)

    def on_close(self):
        # remove clients from waiting set
        SocketHandler.waiters.remove(self)

    def on_message(self, message):
        # clients are not supposed to send message
        logging.info(f"Not expected message: {message}")

    @classmethod
    def boadcast_message(cls, message):
        logging.info(f"Broadcasting message: {message}")

        # send message to all clients waiting on the socket
        for waiter in cls.waiters:
            try:
                waiter.write_message(message)
            except:
                logging.error("Error sending message", exc_info=True)


@gen.coroutine
def register_message(host, port):
    """
    Listen on sum server (host, port) and pass the data to the websocket
    """
    # create stream connection to the server
    stream = yield TCPClient().connect(host, port)
    logger.info(f"Listening to message on server: {host}:{port}")

    while True:
        try:
            # read message from stream connection
            message = yield stream.read_until(b"\n")
            logger.info(f"Register message: {message}")

            # pass message to the websocket
            SocketHandler.boadcast_message(message)
        except StreamClosedError:
            logger.error(f"Lost connection to the server: {host}:{port}")
            break
        except Exception as e:
            print(e)


def main():
    options.parse_command_line()

    # start webapp
    app = Application()
    app.listen(options.web_port)

    # start message registration to the websocket
    register_message(options.listen_host, options.listen_port)

    # start loop
    IOLoop.current().start()


if __name__ == "__main__":
    main()
