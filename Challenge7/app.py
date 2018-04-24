#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
DEVOPS Server
"""

# Standard Libraries
import logging
import os
# Thirdparty Libraries
from tornado import gen
from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import define, options
import redis


# Configuration
define("port",  default=80, help="HTTP port for the app")
logger = logging.getLogger(__name__)

# Storage initialization
r = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0)
r.set('pending', 0)


class MainHandler(web.RequestHandler):
    """
    Handler for route /
    """
    @gen.coroutine
    def get(self):
        self.set_status(200)
        self.write("Ok")

class CheckHandler(web.RequestHandler):
    """
    Handler for route /check
    """
    @gen.coroutine
    def get(self, millis):
        try:
            millis = int(millis)
        except ValueError:
            self.set_status(400)
            yield self.write("FAIL")
            return

        if not 1 <= millis <= 20000:
            self.set_status(400)
            yield self.write("FAIL")
            return

        yield self.wait_millis(millis)

    @gen.coroutine
    def wait_millis(self, millis):
        try:
            pending = int(r.get('pending'))
        except ValueError:
            pending = 0
        r.set('pending', pending+1)

        yield gen.sleep(millis/1000)
        self.set_status(201)
        yield self.write("CHECKED")

        try:
            pending = int(r.get('pending'))
        except ValueError:
            pending = 0
        r.set('pending', pending-1)

class StatsHandler(web.RequestHandler):
    """
    Handler for route /Stats
    """
    @gen.coroutine
    def get(self):
        try:
            pending = int(r.get('pending'))
        except ValueError:
            pending = 0

        self.set_status(200)
        yield self.write("{}".format(pending))


def main():
    options.parse_command_line()
    port = options.port

    app = web.Application([
        (r"/", MainHandler),
        (r"/check/(.*)", CheckHandler),
        (r"/stats", StatsHandler),
    ])

    server = HTTPServer(app)
    server.bind(port)
    server.start(0)    # Number of process to be forked, 0 equals number of cpu
    logger.info("Start at port: {}".format(port))

    IOLoop.current().start()


if __name__ == "__main__":
    main()
