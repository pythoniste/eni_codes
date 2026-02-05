#!/usr/bin/python3

from pysimplesoap.server import SoapDispatcher, SOAPHandler
from http.server import HTTPServer

def hello(name):
    return {'message': 'hello %s' % name}

dispatcher = SoapDispatcher(
    'my_dispatcher',
    location = "http://localhost:8008/",
    action = 'http://localhost:8008/', # SOAPAction
    namespace = "http://example.com/sample.wsdl", prefix="ns0",
    trace = True,
    ns = True)

dispatcher.register_function('Hello', hello,
    returns={'Message': str}, 
    args={'name': str})

if __name__ == "__main__":
    server = HTTPServer(("", 8008), SOAPHandler)
    server.dispatcher = dispatcher
    server.serve_forever()

