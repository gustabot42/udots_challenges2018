#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Webapp and web socket for registed sum server
"""

# Standard libraries
import logging
from random import random, randint
# Thirdparty libraries
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.tcpclient import TCPClient
from tornado.options import options, define


# Configurations
define("host", default="localhost", help="TCP sum server host")
define("port", default=27877, help="TCP sum server port")
define("num_clients", default=2, help="Number of clients to generate")
logger = logging.getLogger(__name__)


@gen.coroutine
def send_data(id, period_seconds=None):
    """
    Clients that send data to server
    """
    if not period_seconds:
        period_seconds = random()

    # start connection to the server
    stream = yield TCPClient().connect(options.host, options.port)
    logger.info(f"Client connected to server: {id}")

    while True:
        data = randint(0, 20)
        try:
            # send data as a messange to the server
            yield stream.write(f"{data}\n".encode('UTF-8'))
            logger.info(f"Client sent data: {id}, {data}")
        except StreamClosedError:
            logger.error(f"Lost connection to the server: {host}:{port}")
            break
        except Exception as e:
            print(e)

        # wait for period en seconds to send next data
        yield gen.sleep(period_seconds)


if __name__ == "__main__":
    options.parse_command_line()

    for id in range(options.num_clients):
        send_data(id)

    IOLoop.current().start()
