from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol


class EchoClient(DatagramProtocol):
    nb = 0
   
    def startProtocol(self):
        self.transport.connect('127.0.0.1', 8000)
        self.transport.write(b"Hello!")

    def datagramReceived(self, datagram, host):
        print('Datagram received: ', repr(datagram))
        if self.nb > 9:
            reactor.stop()
            return
        self.nb += 1
        self.transport.write(f"This is message #{self.nb}".encode("utf-8"))


def main():
    t = reactor.listenUDP(0, EchoClient())
    reactor.run()


if __name__ == '__main__':
    main()
