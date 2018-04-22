#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Sum Server
"""

# Standard Libraries
from collections import defaultdict
import json
import logging
# Thirdparty Libraries
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer
from tornado.options import options, define

# Configuration
define("listen_port", default=27877, help="TCP port to listen on")
define("write_port",  default=27878, help="TCP port to write to")
logger = logging.getLogger(__name__)

# Sum storage (Key value database)
clients_sum = defaultdict(int)

class ListenServer(TCPServer):
    @gen.coroutine
    def handle_stream(self, stream, address):
        ip, port, *_ = address
        while True:
            try:
                data = yield stream.read_until(b"\n")
                data = int(data)
                clients_sum[port] += data
                logger.info(f"Received client, data: {port}, {data}")
            except StreamClosedError:
                clients_sum.pop(port)
                logger.warning(f"Lost data client at port: {port}")
                break
            except Exception as e:
                print(e)


class WriteServer(TCPServer):
    def __init__(self):
        super().__init__()
        self._streams = set()
        self.boadcast()

    @gen.coroutine
    def handle_stream(self, stream, address):
        self._streams.add((stream, address))
        logger.info(f"Broadcasting to port: address[1]")

    @gen.coroutine
    def boadcast(self):
        while True:
            sums = json.dumps(clients_sum)
            for k in clients_sum:
                clients_sum[k] = 0

            message = f"{sums}\r\n".encode('UTF-8')
            for stream, address in self._streams:
                try:
                    yield stream.write(message)
                except StreamClosedError:
                    self._streams.remove((stream, address))
                    logger.warning(f"Lost listen client at port: {address[1]}")
                    break
                except Exception as e:
                    print(e)

            logger.info(f"Broadcasted sums: {sums}")
            yield gen.sleep(1)


if __name__ == "__main__":
    options.parse_command_line()

    listenserver = ListenServer()
    listenserver.listen(options.listen_port)
    logger.info(f"Listening on TCP port {options.listen_port}")

    writeserver = WriteServer()
    writeserver.listen(options.write_port)
    logger.info(f"Writing on TCP port {options.write_port}")

    IOLoop.current().start()
