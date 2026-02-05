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

    def connection_made(self, transport):
        self.transport = transport
        self.logger = logging.getLogger("EchoServerProtocol")
        coloredlogs.install(level="DEBUG", logger=self.logger)
        self.logger.debug("connection made")

    def datagram_received(self, data, addr):
        print(self)
        self.logger.debug(f"received {data.decode()!r} from {addr}")
        self.transport.sendto(data, addr)
        self.logger.debug(f"sent {data.decode()!r}")


async def main():
    event_loop = asyncio.get_running_loop()

    server_factory = event_loop.create_datagram_endpoint(EchoServerProtocol, local_addr=SERVER_ADDRESS)
    transport, protocol = await server_factory
    main_logger.debug(f"starting up on {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}")

    future = event_loop.create_future()
    event_loop.add_signal_handler(signal.SIGINT, future.set_result, None)

    try:
        await future
    finally:
        main_logger.debug("closing server")
        event_loop.remove_signal_handler(signal.SIGINT)
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())

