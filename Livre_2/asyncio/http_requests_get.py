import asyncio
from aiohttp import ClientSession

URLS = [
    "http://python.org/",
    "http://inspyration.org/",
    "http://eni.fr/",
]

async def get(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()
            print(response)

async def main():
    await asyncio.gather(*(get(url) for url in URLS))

if __name__ == "__main__":
    asyncio.run(main())

