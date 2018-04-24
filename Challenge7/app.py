#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Webapp and web socket for registed sum server
"""

# Standard Libraries
from uuid import uuid4 as uuid
import logging
import os.path
# Thirdparty Libraries
from tornado import gen
from tornado import web
from tornado.ioloop import IOLoop
from tornado.options import define, options


define("port",  default=8800, help="HTTP port for the app")
logger = logging.getLogger(__name__)


class MainHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.set_status(200)
        self.write("Ok")

class CheckHandler(web.RequestHandler):
    pending = set()

    @gen.coroutine
    def get(self, millis):
        millis = int(millis)

        if not 1 <= millis <= 20000:
            self.set_status(400)
            yield self.write("FAIL")
            return

        yield self.wait_millis(millis)

    @gen.coroutine
    def wait_millis(self, millis):
        _uuid = uuid()
        CheckHandler.pending.add(_uuid)

        yield gen.sleep(millis/1000)

        self.set_status(201)
        yield self.write("CHECKED")

        CheckHandler.pending.remove(_uuid)


class StatsHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        amount_pending = len(CheckHandler.pending)

        self.set_status(200)
        yield self.write(f"{amount_pending}")


def main():
    options.parse_command_line()
    port = options.port

    application = web.Application([
        (r"/", MainHandler),
        (r"/check/(.*)", CheckHandler),
        (r"/stats", StatsHandler),
    ])

    application.listen(port)
    logger.info(f"Start at port: {port}")

    IOLoop.current().start()


if __name__ == "__main__":
    main()
