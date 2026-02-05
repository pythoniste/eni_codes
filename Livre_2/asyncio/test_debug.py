import argparse
import asyncio
import logging
import coloredlogs
import sys
import time
import warnings


logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)7s: %(message)s",
    stream=sys.stderr,
)
main_logger = logging.getLogger("main")
logger_format = "%(asctime)s,%(msecs)03d %(message)s"
coloredlogs.install(fmt=logger_format, level="DEBUG", logger=main_logger)


async def coroutine_not_awaited():
    main_logger.info("task not awaited starting")
    time.sleep(5)  # using time.sleep, not asyncio.sleep
    main_logger.info("task not awaited completed")

async def coroutine_quite_slow():
    main_logger.info("task quite slow starting")
    time.sleep(0.09)  # using time.sleep, not asyncio.sleep
    main_logger.info("task quite slow completed")

async def coroutine_very_slow():
    main_logger.info("task very slow starting")
    time.sleep(0.1)  # using time.sleep, not asyncio.sleep
    main_logger.info("task very slow completed")


async def main_coroutine_old(loop):
    main_logger.info("main old-style coroutine starting")
    await asyncio.ensure_future(loop.create_task(coroutine_quite_slow()))
    main_logger.info("main old-style coroutine completed")


def main_old(debug, warning, slow):
    main_logger.info("Python old style")
    event_loop = asyncio.get_event_loop()
    if debug:
        main_logger.debug("debug enabled")
        event_loop.set_debug(True)
    else:
        main_logger.debug("debug is disabled")

    if warning:
        main_logger.debug("warning enabled")
        warnings.simplefilter("always", ResourceWarning)
    elif warning is False:
        main_logger.debug("warning disabled")
        warnings.simplefilter("ignore")
    else:
        main_logger.debug("warning are in defaults setting")

    main_logger.debug(f"setting slow_callback_duration to {slow}")
    event_loop.slow_callback_duration = slow

    event_loop.run_until_complete(main_coroutine_old(event_loop))


async def main_coroutine_37():
    main_logger.info("main 3.7-style coroutine starting")
    task1 = asyncio.create_task(coroutine_very_slow())
    task2 = asyncio.create_task(coroutine_quite_slow())
    await task1
    await task2
    coroutine_not_awaited()
    main_logger.info("main 3.7-style coroutine completed")


async def main_37(debug, warning, slow):
    main_logger.info("Python 3.7 style")
    event_loop = asyncio.get_running_loop()
    if debug:
        main_logger.debug("debug is enabled")
        event_loop.set_debug(True)
    else:
        main_logger.debug("debug is disabled")

    if warning:
        main_logger.debug("warning enabled")
        warnings.simplefilter("always", ResourceWarning)
        warnings.simplefilter("always", RuntimeWarning)
    elif warning is False:
        main_logger.debug("warning disabled")
        warnings.simplefilter("ignore")
    else:
        main_logger.debug("warning are in defaults setting")

    main_logger.debug(f"setting slow_callback_duration to {slow}")
    event_loop.slow_callback_duration = slow

    await main_coroutine_37()


def proxy_main(args):
    if args.warnings:
        warnings = True
    elif args.disable_warnings:
        warnings = False
    else:
        warnings = None
    if args.old:
        main_old(args.debug, warnings, args.slow)
    else:
        asyncio.run(main_37(args.debug, warnings, args.slow))


def get_parser():
    parser = argparse.ArgumentParser("debugging asyncio")
    parser.add_argument(
        "-o",
        dest="old",
        help="use old style method",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-d",
        dest="debug",
        help="activate debug on loop",
        default=False,
        action="store_true",
    )
    warning_group = parser.add_mutually_exclusive_group(required=False)
    warning_group.add_argument(
        "-w",
        dest="warnings",
        help="activate some warnings",
        default=False,
        action="store_true",
    )
    warning_group.add_argument(
        "-i",
        dest="disable_warnings",
        help="deactivate all warnings",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-s",
        dest="slow",
        help="slow callback value",
        default=0.1,
        type=float,
    )
    parser.set_defaults(func=proxy_main)
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)

