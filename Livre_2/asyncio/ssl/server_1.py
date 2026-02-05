import asyncio
import logging
import coloredlogs
import sys
import signal
import ssl


SERVER_ADDRESS = ("localhost", 8040)

main_logger = logging.getLogger("main")
logger_format = "%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s"
coloredlogs.install(fmt=logger_format, level="DEBUG", logger=main_logger)


class EchoServerProtocol(asyncio.Protocol):

    instances = set()

    def connection_made(self, transport):
        self.instances.add(self)
        self.transport = transport
        self.address = transport.get_extra_info("peername")
        self.logger = logging.getLogger(f"Client {self.address}")
        coloredlogs.install(level="DEBUG", logger=self.logger)
        self.logger.debug("connection made")
        self.logger.debug(f"transport can EOF? {self.transport.can_write_eof()}")

    def data_received(self, data):
        self.logger.debug(f"received {data!r} from {self.address}")
        terminate = data.endswith(b"\x00")
        if terminate:
            data = data.rstrip(b"\x00")
            print(f"Terminate detected, closing transport soon")
        if data:
            self.transport.write(data)
            self.logger.debug(f"sent {data!r}")
        if terminate:
            self.eof_received()

    def eof_received(self):
        self.logger.debug(f"EOF received for {self.address}")
        self.transport.close()

    @classmethod
    def eof_received_for_all_instances(cls):
        for instance in cls.instances:
            instance.eof_received()

    def connection_lost(self, exc):
        if exc:
            self.logger.error(f"ERROR: {exc}")
        else:
            self.logger.debug("closing")
        self.instances.discard(self)
        super().connection_lost(exc)


async def main():
    event_loop = asyncio.get_running_loop()

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.check_hostname = False
    ssl_context.load_cert_chain("my.crt", "my.key")

    server_factory = event_loop.create_server(EchoServerProtocol, *SERVER_ADDRESS, ssl=ssl_context)
    server = await server_factory
    main_logger.debug(f"starting up on {SERVER_ADDRESS[0]} port {SERVER_ADDRESS[1]}")

    event_loop.add_signal_handler(signal.SIGINT, EchoServerProtocol.eof_received_for_all_instances)

    future = event_loop.create_future()
    event_loop.add_signal_handler(signal.SIGINT, future.set_result, None)

    try:
        await future
    finally:
        main_logger.debug("closing server")
        event_loop.remove_signal_handler(signal.SIGINT)
        server.close()
        await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())

