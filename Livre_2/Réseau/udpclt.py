#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de client UDP utilisant le serveur réalisé avec socket
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

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(params)

messages = [
	b'1cle1|valeur1',	# Ajout donnée
	b'1cle2|valeur2',	# Ajout donnée
	b'0cle1',		# Ne devrait pas fonctionner
	b'cle1',		# Non conforme sur premier byte
	b'1clevaleur',		# Ajout non correctement formaté
	b'1cle|valeur|',	# Ajout non correctement formaté
	b'1cle1|valeur42',	# Mise à jour de donnée
	b'2cle1',		# Suppression de la donnée
	b'3',			# Extinction du serveur
]

for m in messages:
	print("Envoi d'un message %s" % m)
	#s.send(m)
	s.sendto(m, params)
#s.close()
