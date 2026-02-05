from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ServerFactory


class Echo(Protocol):

    def dataReceived(self, data):
        self.transport.write(data)


def main():
    """This runs the protocol on port 8000"""
    factory = ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000,factory)
    reactor.run()


if __name__ == '__main__':
    main()
