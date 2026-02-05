from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol


class Echo(DatagramProtocol):

    def datagramReceived(self, datagram, address):
        self.transport.write(datagram, address)


def main():
    reactor.listenUDP(8000, Echo())
    reactor.run()


if __name__ == '__main__':
    main()
