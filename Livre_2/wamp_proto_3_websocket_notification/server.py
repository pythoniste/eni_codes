import sqlite3
import json
import logging
import coloredlogs
from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory


logger = logging.getLogger("notifications")
coloredlogs.install(level='DEBUG', logger=logger)


DB_NAME = "db.sqlite"


class AbstractTrackingServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sessions (peer, start, end, nb) VALUES (?, datetime('now'), null, 0)",
                       (request.peer,))
        conn.commit()
        conn.close()
        logger.info("Client connecting: {0}".format(request.peer))

    async def onOpen(self):
        logger.info("WebSocket connection open.")
        while True:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) AS active_count FROM sessions WHERE end is null")
            active_count = cursor.fetchone()[0]
            conn.close()
            logger.debug("There is {} active sessions.".format(active_count))
            self.sendMessage(json.dumps({"topic": "active_count", "active_count": active_count}).encode("utf-8"))
            await asyncio.sleep(1)

    def onMessage(self, payload, isBinary):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT nb FROM sessions WHERE peer=? AND end is null", (self.peer,))
        try:
            nb = cursor.fetchone()[0]
        except:
            logger.error("Error while checking on an session that should exists and is not found in the DB")
        else:
            logger.info("{} just sent message #{}".format(self.peer, nb+1))
            cursor.execute("UPDATE sessions SET nb=? WHERE peer=? AND end is null", (nb+1, self.peer))
            conn.commit()
        conn.close()

        if isBinary:
            responseIsBinary, result = self.onMessageBinary(payload)
        else:
            payload = payload.decode("utf-8")
            try:
                payload = json.loads(payload)
            except:
                responseIsBinary, result = self.onMessageText(payload)
            else:
                responseIsBinary, result = self.onMessageJson(payload)
                result = json.dumps(result)
            result = result.encode("utf-8")

        self.sendMessage(result, responseIsBinary)

    def onMessageBinary(self, payload):
        raise NotImplementedError

    def onMessageText(self, payload):
        raise NotImplementedError

    def onMessageJson(self, payload):
        raise NotImplementedError

    def onClose(self, wasClean, code, reason):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE sessions SET end=datetime('now') WHERE peer=? AND end is null",
                       (self.peer,))
        conn.commit()
        cursor = conn.cursor()
        logger.info("client exiting, {0}".format(self.peer))
        cursor.execute("select * from sessions")
        logger.debug(cursor.fetchall())
        conn.close()

        print("WebSocket connection closed: {0}".format(reason))


class AbstractTrackingJSONOnlyServerProtocol(AbstractTrackingServerProtocol):

    def onMessageBinary(self, payload):
        message = "Binary message received: {0} bytes, format not supported".format(len(payload))
        logger.error(message)
        return False, json.dumps({"success": False,
                                  "payload": payload.decode('utf8').replace("'", '"'),
                                  "message": message}).encode("utf-8")

    def onMessageText(self, payload):
        message = "Text message received: {0}, format not supported".format(payload)
        logger.error(message)
        return False, json.dumps({"success": False, "payload": payload, "message": message})


class TestServerProtocol(AbstractTrackingJSONOnlyServerProtocol):

    def onMessageJson(self, payload):
        logger.debug("JSON message received: {0}".format(payload))
        # Do something
        return False, {"success": True, "payload": payload}


if __name__ == '__main__':
    import asyncio

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = TestServerProtocol

    event_loop = asyncio.get_event_loop()
    coroutine = event_loop.create_server(factory, '0.0.0.0', 9000)
    server = event_loop.run_until_complete(coroutine)

    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        event_loop.close()

