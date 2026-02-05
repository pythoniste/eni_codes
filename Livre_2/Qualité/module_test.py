#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Module de test

Ce module a pour objectif de montrer comment
utiliser les outils liés à la documentation
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"

def carre(x):
	"""Retourne le carré de x"""
	return x**2

def cube(x):
	"""Retourne le cube de x"""

def puissance(x, y):
	"""Retourne la puissance y de x"""
	return x**y

class Wrapper:
	"""Classe qui permet de faire des calculs de puissance"""
	def puissance(self, x, y):
		"""Méthode pour le calcul"""
		if y == 2:
			return carre(x)
		elif y == 3:
			return cube(x)
		else:
			return puissance(x, y)


