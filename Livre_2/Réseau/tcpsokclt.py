#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de client TCP utilisant le serveur socketserver
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

messages = [
	b'1cle1|valeur1\n',	# Ajout donnée
	b'1cle2|valeur2\n',	# Ajout donnée
	b'0cle1\n',		# Demande de clé
	b'cle1\n',		# Non conforme sur premier byte
	b'0cle3\n',		# Clé non existante
	b'1clevaleur\n',	# Ajout non correctement formaté
	b'1cle|valeur|\n',	# Ajout non correctement formaté
	b'1cle1|valeur42\n',	# Mise à jour de donnée
	b'0cle1\n',		# On devrait avoir la nouvelle donnée
]

for m in messages:
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(params)
	print("Envoi d'un message %s" % m)
	s.send(m)
	data = s.recv(BUFFER_SIZE)
	if len(data) == 0:
		print('\tPas de réponses')
	elif data[0] == 48:
		print('\tMessage non correctement transmis')
	elif data[0] == 49:
		print('\tDonnée transmise au serveur')
	else:
		print('\tDonnée récupérée du serveur : %s' % data)
	s.close()
