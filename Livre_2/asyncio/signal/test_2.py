import asyncio
import functools
import os
import signal


SIGNAL_NAMES = ("SIGINT", "SIGHUP", "SIGUSR1")


def signal_handler(name):
    print(f"signal {name!r} handled")


async def send_signals():
    pid = os.getpid()
    print(f"starting send_signals for {pid}")

    for name in SIGNAL_NAMES:
        print(f"Sending signal {name} ...", end="")
        os.kill(pid, getattr(signal, name))
        print("Done")
        await asyncio.sleep(0.01)
    return

async def main():
    event_loop = asyncio.get_event_loop()

    for signal_name in SIGNAL_NAMES:
        event_loop.add_signal_handler(
            getattr(signal, signal_name),
            functools.partial(signal_handler, name=signal_name),
        )

    await send_signals()


if __name__ == "__main__":
    asyncio.run(main())

