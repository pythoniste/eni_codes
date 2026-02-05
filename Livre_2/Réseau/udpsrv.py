#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur UDP utilisant socket
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


params = ('127.0.0.1', 8808)
BUFFER_SIZE = 1024 # default

donnees = {}

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#, socket.SOCK_STREAM)
s.bind(params)
# Les lignes suivantes n'ont pas de sens en UDP:
#s.listen(1)
#conn, addr = s.accept()
#print('Connexion acceptée: %s' % str(addr))

while True:
	#data = conn.recv(BUFFER_SIZE)
	data, addr = s.recvfrom(BUFFER_SIZE)
	print('Connexion reçue: %s' % str(addr))
	print('Donnée reçue: %s' % data)
	if data[0] == 49:
		d = data[1:].split(b'|')
		if len(d) != 2:
			print('\tDonnée non conforme')
			continue
		k, v = d[0], d[1]
		donnees[k] = v
		print('\tDonnée mise à jour')
	elif data[0] == 50:
		d = data[1:]
		if d in donnees.keys():
			del donnees[d]
	elif data[0] == 51:
		break
	else:
		print('\tDonnée non conforme %s' % data[0])
#conn.close()
