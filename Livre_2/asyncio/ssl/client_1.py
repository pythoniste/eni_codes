import asyncio
import functools
import logging
import coloredlogs
import sys
import signal
import ssl


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


class EchoClientProtocol(asyncio.Protocol):

    instances = set()

    def __init__(self, loop, future):
        super().__init__()
        self.instances.add(self)
        self.loop = loop
        self.logger = logging.getLogger("EchoClient")
        coloredlogs.install(fmt=logger_format, level="DEBUG", logger=self.logger)
        self.future = future

    async def read_from_input(self):
        try:
            while True:
                msg = await ainput(self.loop, "?")
                if not msg:
                    self.transport.write(b"\x00")  # send EOF
                else:
                    self.transport.write(msg)
                self.logger.debug(f"sending '{msg!r}'")
        except KeyboardInterrupt:
            print("Quitting client")
        finally:
            print("Exiting client")

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info("peername")
        self.logger.debug(f"connecting to {self.address[0]}:{self.address[1]}")
        self.task = self.loop.create_task(self.read_from_input())

    def data_received(self, data):
        self.logger.debug(f"received {data!r}")

    def eof_received(self):
        self.logger.debug("received EOF")
        if not self.future.done():
            self.future.set_result(True)

    @classmethod
    def eof_received_for_all_instances(cls):
        for instance in cls.instances:
            instance.eof_received()

    def connection_lost(self, exc):
        self.logger.debug("server closed connection")
        self.transport.close()
        if not self.future.done():
            self.future.set_result(True)
        self.instances.discard(self)
        super().connection_lost(exc)


async def main():
    event_loop = asyncio.get_running_loop()

    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH,
    )
    ssl_context.check_hostname = False
    ssl_context.load_verify_locations('my.crt')

    client_completed = event_loop.create_future()

    client_factory = functools.partial(
        EchoClientProtocol,
        loop=event_loop,
        future=client_completed,
    )

    factory_coroutine = event_loop.create_connection(
        client_factory,
        *SERVER_ADDRESS,
        ssl=ssl_context,
    )

    event_loop.add_signal_handler(signal.SIGINT, EchoClientProtocol.eof_received_for_all_instances)

    event_loop.add_signal_handler(signal.SIGINT, client_completed.set_result, True)

    main_logger.debug("waiting for client to complete")

    await factory_coroutine
    try:
        await client_completed
    finally:
        event_loop.remove_signal_handler(signal.SIGINT)


if __name__ == "__main__":
    asyncio.run(main())

