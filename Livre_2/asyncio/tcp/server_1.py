import asyncio
import logging
import coloredlogs
import sys

SERVER_ADDRESS = ("localhost", 8040)

main_logger = logging.getLogger("main")
logger_format = "%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s"
coloredlogs.install(fmt=logger_format, level="DEBUG", logger=main_logger)


class EchoServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info("peername")
        self.logger = logging.getLogger(f"Client {self.address}")
        coloredlogs.install(fmt=logger_format, level="DEBUG", logger=self.logger)
        self.logger.debug("connection made")

    def data_received(self, data):
        self.logger.debug(f"received {data!r} from {self.address}")
        self.transport.write(data)
        self.logger.debug(f"sent {data!r}")

    def eof_received(self):
        self.logger.debug("received EOF")
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, exc):
        if exc:
            self.logger.error(f"ERROR: {exc}")
        else:
            self.logger.debug("closing")
        super().connection_lost(exc)


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    server_factory = event_loop.create_server(EchoServerProtocol, *SERVER_ADDRESS)
    server = event_loop.run_until_complete(server_factory)
    main_logger.debug(f"starting up on {SERVER_ADDRESS[0]} port {SERVER_ADDRESS[1]}")

    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        main_logger.debug("closing server")
        server.close()
        event_loop.run_until_complete(server.wait_closed())
        main_logger.debug("closing event loop")
        event_loop.close()

