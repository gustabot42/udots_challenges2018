#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import logging
import os.path

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpclient import TCPClient
import tornado.web
import tornado.websocket


from tornado.options import define, options

define("web_port", default=8899, help="Webapp run on the given port", type=int)
define("listen_host", default='localhost', help="Listen to the given host", type=int)
define("listen_port", default=27878, help="Listen on the given port", type=int)
logger = logging.getLogger(__name__)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/socket", SocketHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=ChatSocketHandler.cache)


class SocketHandler(tornado.websocket.WebSocketHandler):

    waiters = set()

    def open(self):
        SocketHandler.waiters.add(self)

    def on_close(self):
        SocketHandler.waiters.remove(self)

    def on_message(self, message):
        logging.info(f"Not expected message: {message}")

    @classmethod
    def boadcast_message(cls, message):
        logging.info(f"Broadcasting message: {message}")
        for waiter in cls.waiters:
            try:
                waiter.write_message(message)
            except:
                logging.error("Error sending message", exc_info=True)


@gen.coroutine
def register_message(host, port):
    stream = yield TCPClient().connect(host, port)
    logger.info(f"Listening to message on server: {host}:{port}")

    while True:
        try:
            message = yield stream.read_until(b"\n")
            logger.info(f"Register message: {message}")
            SocketHandler.boadcast_message(message)
        except StreamClosedError:
            logger.error(f"Lost connection to the server: {host}:{port}")
            break
        except Exception as e:
            print(e)


def main():
    options.parse_command_line()
    app = Application()
    app.listen(options.web_port)

    register_message(options.listen_host, options.listen_port)

    IOLoop.current().start()


if __name__ == "__main__":
    main()
