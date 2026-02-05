import asyncio
import logging
import coloredlogs
import sys
import signal
from functools import partial
from contextvars import ContextVar, copy_context


main_logger = logging.getLogger("main")
logger_format = "%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s"
coloredlogs.install(fmt=logger_format, level="DEBUG", logger=main_logger)


nb = ContextVar("How many ?", default=0)
nb.set(0)
ctx = copy_context()


async def aside_value():
    main_logger.info(f"aside_value starting with   {nb.get()!r}")  
    nb.set(await asyncio.sleep(1, result=42))
    main_logger.info(f"aside_value ending with     {nb.get()!r}")  

def used_value():
    main_logger.info(f"used_value starting with    {nb.get()!r}")  
    nb.set(10)
    main_logger.info(f"used_value ending with      {nb.get()!r}")

async def testing_tokens():
    await asyncio.sleep(0.1)
    main_logger.info(f"using token starting with: {nb.get()!r}")  
    token_1 = nb.set(await asyncio.sleep(0.01, result=1))
    main_logger.info(f"token 1: from {token_1.old_value} > {nb.get()!r}")  
    token_2 = nb.set(await asyncio.sleep(0.01, result=2))
    main_logger.info(f"token 2: from {token_2.old_value} > {nb.get()!r}")  
    token_3 = nb.set(await asyncio.sleep(0.01, result=3))
    main_logger.info(f"token 3: from {token_3.old_value} > {nb.get()!r}")  
    nb.reset(token_3)
    main_logger.info(f"using token 3: {nb.get()!r}")  
    nb.reset(token_1)
    main_logger.info(f"using token 1: {nb.get()!r}")  
    nb.reset(token_2)
    main_logger.info(f"using token 1: {nb.get()!r}")  
    nb.reset(token_1)  # this will cause RuntimeError


def print_callback(crut):
    main_logger.info(f"Callback said               {nb.get()!r}")


async def main():
    event_loop = asyncio.get_running_loop()
    task = asyncio.create_task(aside_value())
    task.add_done_callback(print_callback, context=ctx)

    ctx.run(used_value)
    await task

    task = asyncio.create_task(testing_tokens())
    await task


if __name__ == "__main__":
    asyncio.run(main())

