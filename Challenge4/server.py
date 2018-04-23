#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Sum Server listen a writer
"""

# Standard Libraries
from collections import defaultdict
import json
import logging
# Thirdparty Libraries
from tornado import gen
from tornado.escape import json_encode
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.options import options, define
from tornado.tcpserver import TCPServer


# Configuration
define("listen_port", default=27877, help="TCP port to listen on")
define("write_port",  default=27878, help="TCP port to write to")
logger = logging.getLogger(__name__)

# Sum storage (Key value database)
clients_sum = defaultdict(int)

class ListenServer(TCPServer):
    """
    Listen data integers and sum it,
    the sum is acumulated in a key-value storage 'clients_sum' with address port as key
    """
    @gen.coroutine
    def handle_stream(self, stream, address):
        ip, port, *_ = address
        clients_sum[port] += 0

        while True:
            try:
                # Read data as integer and check if valid
                data = yield stream.read_until(b"\n")
                data = int(data)
                if not 0 <= data <= 20:
                    logger.info(f"Data out of range, client, data: {port}, {data}")
                    raise StreamClosedError

                # Acumulate data in storage
                clients_sum[port] += int(data)

                logger.info(f"Received client, data: {port}, {data}")
            except StreamClosedError:
                # Remove from client from storage if connection lost
                clients_sum.pop(port)
                logger.warning(f"Lost data client at port: {port}")
                break
            except Exception as e:
                print(e)


class WriteServer(TCPServer):
    """
    Write data sums as json from key-value store clients_sum
    """
    def __init__(self):
        super().__init__()
        # Set of streams to broadcast to
        self._streams = set()
        # Corutine for broadcast
        self.broadcast()

    @gen.coroutine
    def handle_stream(self, stream, address):
        self._streams.add((stream, address))
        logger.info(f"Broadcasting to client on port: address[1]")

    @gen.coroutine
    def broadcast(self):
        while True:
            # get actual sums and reset it
            sums = json_encode(clients_sum)
            for k in clients_sum:
                clients_sum[k] = 0

            # broadcast message to all streams
            message = f"{sums}\r\n".encode('UTF-8')
            for stream, address in self._streams:
                try:
                    yield stream.write(message)
                except StreamClosedError:
                    # remove stream from broadcasting set
                    self._streams.remove((stream, address))
                    logger.warning(f"Lost listen client at port: {address[1]}")
                    break
                except Exception as e:
                    print(e)
            logger.info(f"Broadcasted sums: {sums}")

            # Sleep for 1 second, waiting for sums to acumulate
            yield gen.sleep(1)


if __name__ == "__main__":
    options.parse_command_line()

    # Start listen server
    listenserver = ListenServer()
    listenserver.listen(options.listen_port)
    logger.info(f"Listening on TCP port {options.listen_port}")

    # Start write server
    writeserver = WriteServer()
    writeserver.listen(options.write_port)
    logger.info(f"Writing on TCP port {options.write_port}")

    # Start loop
    IOLoop.current().start()
