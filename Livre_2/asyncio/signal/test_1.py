import asyncio
import signal

async def wait_for_interrupt():
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    loop.add_signal_handler(signal.SIGINT, future.set_result, None)
    try:
        await future
    finally:
        loop.remove_signal_handler(signal.SIGINT)

if __name__ == "__main__":
    asyncio.run(wait_for_interrupt())

