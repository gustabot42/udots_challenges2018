#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
DEVOPS Server
"""

# Standard Libraries
import asyncio
import logging
import os
# Thirdparty Libraries
from tornado import gen
from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import define, options
import aioredis


try:
    REDIS_HOST = os.environ['REDIS_HOST']
except KeyError:
    REDIS_HOST = "localhost"
try:
    REDIS_PORT = os.environ['REDIS_PORT']
except KeyError:
    REDIS_PORT = 6379

PENDING_KEY = 42    # if you are going to use a random number, why not the answer to all.

# Configuration
define("port",  default=88, help="HTTP port for the app")
logger = logging.getLogger(__name__)


class MainHandler(web.RequestHandler):
    """
    Handler for route /
    """
    @asyncio.coroutine
    def get(self):
        self.set_status(200)
        self.write("Ok")

class CheckHandler(web.RequestHandler):
    """
    Handler for route /check
    """
    def initialize(self, redis):
        self.redis = redis

    @asyncio.coroutine
    def get(self, millis):
        try:
            millis = int(millis)
        except ValueError:
            self.set_status(400)
            self.write("FAIL")
            return

        if not 1 <= millis <= 20000:
            self.set_status(400)
            self.write("FAIL")
            return

        yield from self._wait_millis(millis)

    @asyncio.coroutine
    def _wait_millis(self, millis):
        yield from self.redis.incr(PENDING_KEY)

        yield from gen.sleep(millis/1000)
        self.set_status(201)
        self.write("CHECKED")

        yield from self.redis.decr(PENDING_KEY)

class StatsHandler(web.RequestHandler):
    """
    Handler for route /Stats
    """
    def initialize(self, redis):
        self.redis = redis

    @asyncio.coroutine
    def get(self):
        pending = yield from self.redis.get(PENDING_KEY)
        pending = pending.decode()

        self.set_status(200)
        self.write(f"{pending}")


def get_redis_connection(loop):
    # Storage initialization
    return loop.run_until_complete(
        aioredis.create_redis((REDIS_HOST, REDIS_PORT), loop=loop)
    )

def main():
    # get configuration
    options.parse_command_line()
    port = options.port

    ioloop = asyncio.get_event_loop()

    redis = get_redis_connection(ioloop)
    app = web.Application([
        (r"/", MainHandler),
        (r"/check/(.*)", CheckHandler, dict(redis=redis)),
        (r"/stats", StatsHandler, dict(redis=redis)),
    ])

    server = HTTPServer(app)
    server.bind(port)
    server.start()
    logger.info(f"Start at port: {port}")

    ioloop.run_forever()


if __name__ == "__main__":
    main()
