import asyncio
import logging
import coloredlogs
import sys
import signal


SERVER_ADDRESS = ("localhost", 8040)

main_logger = logging.getLogger("main")
coloredlogs.install(fmt="%(name)s: %(message)s", level="DEBUG", logger=main_logger)


async def echo(reader, writer):
    address = writer.get_extra_info("peername")
    logger = logging.getLogger(f"Client {address}")
    coloredlogs.install(fmt="%(name)s: %(message)s", level="DEBUG", logger=logger)
    logger.debug("connection made {address}")

    while True:
        data = await reader.read(128)
        if data:
            logger.debug(f"received {data!r}")
            writer.write(data)
            await writer.drain()
            logger.debug(f"sent {data!r}")
        else:
            logger.debug(f"{address} closing")
            writer.close()
            return


async def main():
    event_loop = asyncio.get_running_loop()
    server_factory = asyncio.start_server(echo, *SERVER_ADDRESS)
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

