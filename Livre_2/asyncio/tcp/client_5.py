import asyncio
import functools
import logging
import coloredlogs
import sys
import signal


SERVER_ADDRESS = ("localhost", 8040)

main_logger = logging.getLogger("main")
coloredlogs.install(level="DEBUG", logger=main_logger)

async def ainput(prompt):
    loop = asyncio.get_running_loop()
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

    except Timeout:
        sys.stdout.write("\n")
        sys.stdout.flush()
        return ""

    finally:
        loop.remove_reader(sys.stdin.fileno())


async def read_from_input(client_completed, writer):
    try:
        while True:
            msg = await ainput("?")
            writer.write(msg)
            if not msg:
                return
    except KeyboardInterrupt:
        print("Quitting client")
    finally:
        print("Exiting client")
        if writer.can_write_eof():
            writer.write_eof()
        await writer.drain()
        client_completed.set_result(True)
        return

async def print_from_server(client_completed, reader):
    while True:
        data = await reader.read(128)
        if data:
            main_logger.debug(f"{data.decode()!r}")
        else:
            main_logger.debug("server closed connection")
            return


async def main():
    event_loop = asyncio.get_running_loop()

    client_completed = event_loop.create_future()

    event_loop.add_signal_handler(signal.SIGINT, client_completed.set_result, True)

    main_logger.debug(f"connecting to {SERVER_ADDRESS[0]} port {SERVER_ADDRESS[1]}")
    reader, writer = await asyncio.open_connection(*SERVER_ADDRESS)
    task_input = event_loop.create_task(read_from_input(client_completed, writer))
    task_output = event_loop.create_task(print_from_server(client_completed, reader))

    event_loop.add_signal_handler(signal.SIGINT, task_input.cancel)

    main_logger.debug("waiting for client to complete")

    try:
        await asyncio.gather(
            client_completed,
            task_input,
            task_output,
            return_exceptions=True,
        )
    finally:
        event_loop.remove_signal_handler(signal.SIGINT)
        writer.close()


if __name__ == "__main__":
    asyncio.run(main())

