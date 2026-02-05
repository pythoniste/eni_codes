import asyncio
import logging
import coloredlogs
import sys
import signal


SERVER_ADDRESS = ("localhost", 8040)

main_logger = logging.getLogger("main")
coloredlogs.install(fmt="%(name)s: %(message)s", level="DEBUG", logger=main_logger)


class EchoServerProtocol(asyncio.Protocol):

    instances = {}

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info("peername")
        self.logger = logging.getLogger(f"Client {self.address}")
        coloredlogs.install(fmt="%(name)s: %(message)s", level="DEBUG", logger=self.logger)
        self.logger.debug("connection made")
        self.instances[self] = "Anonymous"
        for instance in self.instances:
            instance.transport.write(f"! {self.address} entering".encode())

    def data_received(self, data):
        self.logger.debug(f"received {data!r} from {self.address}")
        text = data.decode()
        if text.startswith("!name:"):
            old_name, new_name = self.instances[self], text[6:]
            self.instances[self] = new_name
            self.logger = logging.getLogger(new_name)
            coloredlogs.install(fmt="%(name)s: %(message)s", level="DEBUG", logger=self.logger)
            for instance in self.instances:
                instance.transport.write(f"! {old_name} is now known as {new_name}".encode())
        else:
            for instance in self.instances:
                instance.transport.write(f"{self.instances[self]} > {text}".encode())
                self.logger.debug(f"sent {data!r} to {instance.address}")

    def eof_received(self):
        self.logger.debug("received EOF")
        self.logger.debug(f"{self.address} exiting")
        for instance in self.instances:
            instance.transport.write(f"! {self.address} exiting".encode())
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, exc):
        if exc:
            self.logger.error(f"ERROR: {exc}")
        else:
            self.logger.debug("closing")
        del self.instances[self]
        super().connection_lost(exc)


async def main():
    event_loop = asyncio.get_running_loop()
    server_factory = event_loop.create_server(EchoServerProtocol, *SERVER_ADDRESS)
    server = await server_factory
    main_logger.debug(f"starting up on {SERVER_ADDRESS[0]} port {SERVER_ADDRESS[1]}")

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

