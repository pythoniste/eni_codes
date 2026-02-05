#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur HTTP.
Il se teste à l'aide d'un simple navigateur.
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


from http.server import BaseHTTPRequestHandler, HTTPServer


params = '127.0.0.1', 8016

class HelloHandler(BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.send_response(200)
		self.send_header(b'Content-type', b'text.html')
		self.end_headers()
	def do_GET(self):
		self.do_HEAD()
		self.wfile.write(b"""<html><head><title>Hello World</title></head><body><p>Hello World</p></body></html>""")
	do_POST = do_GET

server = HTTPServer(params, HelloHandler)
server.serve_forever()

