from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory


class EchoClient(Protocol):
    
    def connectionMade(self):
        self.transport.write(b"hello, world!")
    
    def dataReceived(self, data):
        print("Server said:", data)
        self.transport.loseConnection()
    
    def connectionLost(self, reason):
        print("connection lost")


class EchoFactory(ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed")
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print("Connection lost")
        reactor.stop()


def main():
    f = EchoFactory()
    reactor.connectTCP("localhost", 8000, f)
    reactor.run()


if __name__ == '__main__':
    main()
