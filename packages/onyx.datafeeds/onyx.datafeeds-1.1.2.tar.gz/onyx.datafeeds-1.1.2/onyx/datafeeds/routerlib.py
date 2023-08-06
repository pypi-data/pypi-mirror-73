###############################################################################
#
#   Copyright: (c) 2017 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from onyx.core import load_system_configuration, Date

from .utils import encode_message, request_to_uid
from .exceptions import NoDataserverAvailable

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.tcpclient
import tornado.gen

import asyncmc
import socket
import datetime
import random
import logging
import os

RT_TIMEOUT = 300  # in seconds


###############################################################################
class DataRouter(tornado.web.Application):
    # -------------------------------------------------------------------------
    def __init__(self, timeout=60, logger=None, *args, **kwds):
        super().__init__(*args, **kwds)
        self.logger = logger or logging.getLogger(__name__)
        self.timeout = datetime.timedelta(seconds=timeout)

        config = load_system_configuration()
        self.mc_servers = [config.get("memcache", "url")]
        self.dataservers = []

    # -------------------------------------------------------------------------
    def add_dataserver(self, server_id):
        if server_id not in self.dataservers:
            self.dataservers.append(server_id)
            self.logger.info("{0!s} registered "
                "as available server".format(server_id))
            return True
        return False

    # -------------------------------------------------------------------------
    def drop_dataserver(self, server_id, msg):
        self.logger.info("dropping "
            "dataserver {0!s}: {1:s}".format(server_id, msg))
        try:
            self.dataservers.remove(server_id)
        except ValueError:
            pass

    # -------------------------------------------------------------------------
    def select_dataserver(self):
        try:
            return random.choice(self.dataservers)
        except IndexError:
            raise NoDataserverAvailable()

    # -------------------------------------------------------------------------
    def start(self, port=None):
        config = load_system_configuration()
        port = port or config.getint("datafeed", "router_port")

        # --- windows-specific hack: increase the file descriptor limit to
        #     circumvent "too many file descriptors in select()" error
        if os.name == "nt":
            import win32file
            win32file._setmaxstdio(2048)
            assert win32file._getmaxstdio() == 2048

        # --- start HTTP server with an idle_connection_timeout so that idle
        #     connections don't stick around for more than 90 seconds
        http_server = tornado.httpserver.HTTPServer(
            self, idle_connection_timeout=90)
        http_server.listen(port)

        # --- start the memcache-client
        self.cache = asyncmc.Client(
            servers=self.mc_servers, loop=tornado.ioloop.IOLoop.current())

        address = socket.gethostbyname(socket.gethostname())
        self.logger.info("listening on {0!s}:{1!s}".format(address, port))

        try:
            tornado.ioloop.IOLoop.current().start()
        except KeyboardInterrupt:
            tornado.ioloop.IOLoop.current().stop()
        finally:
            self.cleanup()

    # -------------------------------------------------------------------------
    def cleanup(self):
        self.logger.info("shutting down router")

    # -------------------------------------------------------------------------
    async def with_timeout(self, future):
        return await tornado.gen.with_timeout(self.timeout, future)

    # -------------------------------------------------------------------------
    async def fetch(self, req, addr, port):
        client = tornado.tcpclient.TCPClient()
        stream = await self.with_timeout(client.connect(addr, port))

        try:
            await self.with_timeout(stream.write(encode_message(req)))
            response = await self.with_timeout(stream.read_until(b"\n"))
        finally:
            try:
                stream.close()
            except tornado.iostream.StreamClosedError:
                pass

        return response

    # -------------------------------------------------------------------------
    async def process_request(self, req, real_time):
        # --- determine the unique request id, used for caching
        req_uid = request_to_uid(req, real_time)

        # --- first try fetching response from cache
        while True:
            response = await self.cache.get(req_uid)
            if response == "CacheLocked":
                await tornado.gen.sleep(0.25)
            else:
                break

        if response is None:
            # --- no valid data stored in cache, send request to datafeed
            #     router.
            #     NB: we first lock the cache with a timeout and then we only
            #         set the cache if the response is valid.
            await self.cache.set(
                req_uid, "CacheLocked", self.timeout.seconds, noreply=True)

            while True:
                # --- select dataserver or return error if none is available
                try:
                    addr, port = self.select_dataserver()
                except NoDataserverAvailable:
                    resp = {
                        "type": "NoDataserverAvailable",
                        "payload": "Dataservers not available or unresponsive",
                    }
                    return 503, encode_message(resp)

                try:
                    response = await self.fetch(req, addr, port)
                except (tornado.gen.TimeoutError,
                        tornado.iostream.StreamClosedError) as err:
                    # --- connection unresponsive: drop dataserver from list
                    #     and process the request again
                    self.drop_dataserver((addr, port), msg=str(err))
                    continue
                else:
                    break

            if real_time:
                expiry = RT_TIMEOUT
            else:
                expiry = int(Date.today().eod().timestamp())

            await self.cache.set(req_uid, response, expiry, noreply=True)

            self.logger.debug(
                "returning value from dataserver "
                "(rt={0!s}), req_uid='{1!s}'".format(real_time, req_uid))

        else:
            self.logger.debug(
                "returning value from cache (rt={0!s})".format(real_time))

        return 200, response


###############################################################################
class RegistrationHandler(tornado.web.RequestHandler):
    # -------------------------------------------------------------------------
    def put(self):
        self.set_header("Access-Control-Allow-Origin", "*")

        addr = self.get_argument("address")
        port = self.get_argument("port")

        added = self.application.add_dataserver((addr, port))
        if added:
            self.set_status(201)
        else:
            self.set_status(205)


###############################################################################
class BbgBDPHandler(tornado.web.RequestHandler):
    # -------------------------------------------------------------------------
    async def get(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")

        request = {
            "type": "BDP",
            "sec": self.get_argument("sec"),
            "field": self.get_argument("field"),
            "overrides": self.get_argument("overrides", "null"),
        }

        rt = self.get_argument("rt", False)

        status, resp = await self.application.process_request(request, rt)

        self.set_status(status)
        self.write(resp)


###############################################################################
class BbgBDHHandler(tornado.web.RequestHandler):
    # -------------------------------------------------------------------------
    async def get(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")

        request = {
            "type": "BDH",
            "sec": self.get_argument("sec"),
            "field": self.get_argument("field"),
            "start": self.get_argument("start"),
            "end": self.get_argument("end"),
            "adjusted": self.get_argument("adjusted", True),
            "overrides": self.get_argument("overrides", "null"),
        }

        rt = self.get_argument("rt", False)

        status, resp = await self.application.process_request(request, rt)

        self.set_status(status)
        self.write(resp)


###############################################################################
class BbgUniqueIdHandler(tornado.web.RequestHandler):
    # -------------------------------------------------------------------------
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")

        reqtype = self.get_argument("type")
        real_time = self.get_argument("real-time")

        if reqtype == "BDP":
            request = {
                "type": "BDP",
                "sec": self.get_argument("sec"),
                "field": self.get_argument("field"),
                "overrides": self.get_argument("overrides", None),
            }
        elif reqtype == "BDH":
            request = {
                "type": "BDH",
                "sec": self.get_argument("sec"),
                "field": self.get_argument("field"),
                "start": self.get_argument("start"),
                "end": self.get_argument("end"),
                "adjusted": self.get_argument("adjusted", True),
                "overrides": self.get_argument("overrides", None),
            }

        req_uid = request_to_uid(request, real_time)

        self.set_status(200)
        self.write(req_uid)
