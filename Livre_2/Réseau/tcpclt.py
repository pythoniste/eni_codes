#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de client TCP utilisant serveur socket
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

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(params)

messages = [
	b'1cle1|valeur1',	# Ajout donnée
	b'1cle2|valeur2',	# Ajout donnée
	b'0cle1',		# Demande de clé
	b'cle1',		# Non conforme sur premier byte
	b'0cle3',		# Clé non existante
	b'1clevaleur',		# Ajout non correctement formaté
	b'1cle|valeur|',	# Ajout non correctement formaté
	b'1cle1|valeur42',	# Mise à jour de donnée
	b'0cle1',		# On devrait avoir la nouvelle donnée
]

for m in messages:
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
