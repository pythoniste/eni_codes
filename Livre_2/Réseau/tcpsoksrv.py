#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur TCP utilisant socketserver
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"



import socketserver

params = ('127.0.0.1', 8809)

donnees = {}

class ExampleTCPHandler(socketserver.StreamRequestHandler):
	def handle(self):
		self.data = self.rfile.readline().strip()
		print('Donnée reçue: %s' % self.data)
		if self.data[0] == 49:
			d = self.data[1:].split(b'|')
			if len(d) != 2:
				print('\tDonnée non conforme')
				self.wfile.write(b'0\n')
				return
			k, v = d[0], d[1]
			donnees[k] = v
			print('\tDonnée mise à jour')
			self.wfile.write(b'1\n')
		elif self.data[0] == 48:
			d = donnees.get(self.data[1:])
			if d is None:
				print('\tNon disponible')
				self.wfile.write(b'0\n')
				return
			print('\tDonnée renvoyée: %s' % d)
			self.wfile.write(d+b'\n')
		else:
			print('Donnée non conforme %s' % self.data[0])
			self.wfile.write(b'0\n')

if __name__ == '__main__':
	server = socketserver.TCPServer(params, ExampleTCPHandler)
	server.serve_forever()

