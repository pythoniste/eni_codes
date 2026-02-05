import asyncio
import functools
import logging
import coloredlogs

main_logger = logging.getLogger("main")
logger_format = "%(asctime)s,%(msecs)03d %(message)s"
coloredlogs.install(fmt=logger_format, level="DEBUG", logger=main_logger)


class LSProtocol(asyncio.SubprocessProtocol):
    FD_NAMES = ["stdin", "stdout", "stderr"]

    def __init__(self, done_future):
        self.done = done_future
        self.buffer = bytearray()
        super().__init__()

    def connection_made(self, transport):
        main_logger.debug(f"process started {transport.get_pid()}")
        self.transport = transport

    def pipe_data_received(self, fd, data):
        main_logger.debug(f"read {len(data)} bytes from {fd}({self.FD_NAMES[fd]})")
        if fd == 1:
            self.buffer.extend(data)

    def process_exited(self):
        main_logger.debug("process exited")
        return_code = self.transport.get_returncode()
        main_logger.debug(f"return code {return_code}")
        if not return_code:
            cmd_output = bytes(self.buffer).decode()
            results = self._parse_results(cmd_output)
        else:
            results = []
        self.done.set_result((return_code, results))

    def _parse_results(self, output):
        main_logger.debug("parsing results")
        return output.splitlines()


async def main():
    event_loop = asyncio.get_running_loop()

    cmd_done = asyncio.Future(loop=event_loop)
    factory = functools.partial(LSProtocol, cmd_done)
    proc = event_loop.subprocess_exec(
        factory,
        "ls",  # "existe_pas",
        stdin=None,
        stderr=None,
    )
    try:
        main_logger.debug("launching process")
        transport, protocol = await proc
        main_logger.debug("waiting for process to complete")
        await cmd_done
    except Exception as e:
        main_logger.error(f"an exception occurs {e!r}")
    else:
        return_code, results = cmd_done.result()

        if return_code:
            main_logger.error(f"error exit {return_code}")
        else:
            for i, r in enumerate(results):
                print(f"{i:2}: {r}")

    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())

