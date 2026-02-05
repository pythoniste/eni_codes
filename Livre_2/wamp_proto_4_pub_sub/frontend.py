import asyncio
import logging
import coloredlogs
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


logger = logging.getLogger("notifications")
coloredlogs.install(level='DEBUG', logger=logger)


class Component(ApplicationSession):

    async def onJoin(self, details):

        def on_event(i):
            logger.info("Now: {}".format(i))

        await self.subscribe(on_event, u'com.test.topic_clock')

    def onDisconnect(self):
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "test")
    runner.run(Component)

