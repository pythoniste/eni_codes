#!/usr/bin/python3

from pysimplesoap.client import SoapClient, SoapFault

client = SoapClient(
    location = "http://localhost:8008/",
    action = 'http://localhost:8008/', # SOAPAction
    namespace = "http://example.com/sample.wsdl", 
    soap_ns='soap',
    ns = False)

response = client.Hello(name="world")

print(response.Message)

