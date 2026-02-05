from __future__ import print_function

from twisted.protocols.amp import Command, AMP, Integer
from twisted.internet import reactor
from twisted.internet.protocol import Factory

class InvalidResult(Exception):
    pass

class Add(Command):
    arguments = [(b'a', Integer())]
    response = [(b'number', Integer())]

class Sub(Command):
    arguments = [(b'a', Integer())]
    response = [(b'number', Integer())]
    errors = {InvalidResult: b'INVALID_RESULT'}


class DataHandler:
    number = 3


class Number(AMP):

    def add(self, a):
        print('New number {} + {}'.format(DataHandler.number, a))
        DataHandler.number += a
        return {'number': DataHandler.number}
    Add.responder(add)

    def sub(self, a):
        print('New number {} - {}'.format(DataHandler.number, a))
        DataHandler.number -= a
        if DataHandler.number < 0:
            DataHandler.number = 0
            raise InvalidResult()
        return {'number': DataHandler.number}
    Sub.responder(sub)

def main():
    pf = Factory()
    pf.protocol = Number
    reactor.listenTCP(1234, pf)
    print('reactor started')
    reactor.run()

if __name__ == '__main__':
    main()

