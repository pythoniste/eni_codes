#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur TCP utilisant socket
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


import socket


params = ('127.0.0.1', 8809)
BUFFER_SIZE = 1024 # default

donnees = {}

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(params)
s.listen(1)

conn, addr = s.accept()
print('Connexion acceptée: %s' % str(addr))

while 1:
	data = conn.recv(BUFFER_SIZE)
	if not data:
		break
	print('Donnée reçue: %s' % data)
	if data[0] == 49:
		d = data[1:].split(b'|')
		if len(d) != 2:
			print('\tDonnée non conforme')
			conn.send(b'0')
			continue
		k, v = d[0], d[1]
		donnees[k] = v
		print('\tDonnée mise à jour')
		conn.send(b'1')
	elif data[0] == 48:
		d = donnees.get(data[1:])
		if d is None:
			print('\tNon disponible')
			conn.send(b'0')
			continue
		print('\tDonnée renvoyée: %s' % d)
		conn.send(d)
	else:
		print('Donnée non conforme %s' % data[0])
		conn.send(b'0')
conn.close()
