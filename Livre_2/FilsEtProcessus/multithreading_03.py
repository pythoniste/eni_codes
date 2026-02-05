#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Illustration du fonctionnement du module multiprocessing
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


from multiprocessing import Process

from time import sleep


def work(name):
	print('Debut du travail: %s' % name)
	for j in range(2):
		for i in range(10):
			sleep(0.01)
			print('.', sep='', end='')
		print('.')
	print('Fin du travail: %s' % name)

p = Process(target=work, args=('Test',))
p.start()
print('Attente de la fin du processus')
for j in range(4):
	for i in range(10):
		sleep(0.01)
		print('o', sep='', end='')
	print('o')

print('Fin de l\'attente')
p.join()

