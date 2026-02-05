import asyncio
import functools
import logging
import coloredlogs
import sys
import signal


SERVER_ADDRESS = ("localhost", 8040)

main_logger = logging.getLogger("main")
logger_format = "%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s"
coloredlogs.install(fmt=logger_format, level="DEBUG", logger=main_logger)


async def ainput(loop, prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()

    queue = asyncio.Queue()

    def response():
        loop.create_task(queue.put(sys.stdin.readline()))

    loop.add_reader(sys.stdin.fileno(), response)

    try:
        task = loop.create_task(queue.get())
        result = await task
        return result.strip().encode()

    except asyncio.futures.TimeoutError:
        sys.stdout.write("\n")
        sys.stdout.flush()
        return ""

    finally:
        loop.remove_reader(sys.stdin.fileno())


class EchoClient(asyncio.Protocol):

    def __init__(self, loop, future):
        super().__init__()
        self.loop = loop
        self.logger = logging.getLogger("EchoClient")
        coloredlogs.install(fmt=logger_format, level="DEBUG", logger=self.logger)
        self.future = future

    async def read_from_input(self):
        try:
            while True:
                msg = await ainput(self.loop, "?")
                self.transport.write(msg)
                self.logger.debug(f"sending '{msg!r}'")
        except KeyboardInterrupt:
            print("Quitting client")
        finally:
            print("Exiting client")
            if self.transport.can_write_eof():
                self.transport.write_eof()

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info("peername")
        self.logger.debug(f"connecting to {self.address[0]} port {self.address[1]}")
        self.task = self.loop.create_task(self.read_from_input())

    def data_received(self, data):
        self.logger.debug(f"received {data!r}")

    def eof_received(self):
        self.logger.debug("received EOF")
        self.transport.close()
        if not self.future.done():
            self.future.set_result(True)

    def connection_lost(self, exc):
        self.logger.debug("server closed connection")
        self.transport.close()
        if not self.future.done():
            self.future.set_result(True)
        super().connection_lost(exc)


async def main():
    event_loop = asyncio.get_running_loop()

    client_completed = event_loop.create_future()

    client_factory = functools.partial(
        EchoClient,
        loop=event_loop,
        future=client_completed,
    )

    factory_coroutine = event_loop.create_connection(
        client_factory,
        *SERVER_ADDRESS,
    )

    event_loop.add_signal_handler(signal.SIGINT, client_completed.set_result, True)

    main_logger.debug("waiting for client to complete")

    await factory_coroutine
    try:
        await client_completed
    finally:
        event_loop.remove_signal_handler(signal.SIGINT)


if __name__ == "__main__":
    asyncio.run(main())

