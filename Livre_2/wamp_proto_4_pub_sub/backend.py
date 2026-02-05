import asyncio
from datetime import datetime
import logging
import coloredlogs
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


logger = logging.getLogger("notifications")
coloredlogs.install(level='DEBUG', logger=logger)


class Component(ApplicationSession):

    async def onJoin(self, details):
        while True:
            now = datetime.now().strftime("%d %B %Y, %Hh %Mm %Ss")
            logger.info("publish: com.test.topic_clock {}".format(now))
            self.publish("com.test.topic_clock", now)
            await asyncio.sleep(1)


if __name__ == '__main__':
    runner = ApplicationRunner("ws://127.0.0.1:9090/ws", "test")
    runner.run(Component)

