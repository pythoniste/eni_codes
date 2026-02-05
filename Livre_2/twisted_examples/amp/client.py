from __future__ import print_function

from twisted.internet import reactor, defer, endpoints
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols.amp import AMP
from server import Add, Sub, InvalidResult


def doNumber():
    destination = TCP4ClientEndpoint(reactor, '127.0.0.1', 1234)
    addDeferred = connectProtocol(destination, AMP())
    def connected(ampProto):
        return ampProto.callRemote(Add, a=13)
    addDeferred.addCallback(connected)
    def get_number(result):
        return result['number']
    addDeferred.addCallback(get_number)

    subDeferred = connectProtocol(destination, AMP())
    def connected(ampProto):
        return ampProto.callRemote(Sub, a=15)
    subDeferred.addCallback(connected)
    subDeferred.addCallback(get_number)
    def trapInvalidResult(result):
        result.trap(InvalidResult)
        print("Invalid result: returning 0")
        return 0
    subDeferred.addErrback(trapInvalidResult)

    def done(result):
        print('Done with number:', result)
        reactor.stop()
    defer.DeferredList([addDeferred, subDeferred]).addCallback(done)

if __name__ == '__main__':
    doNumber()
    reactor.run()
