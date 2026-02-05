#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Illustration du fonctionnement d'un parseur d'arguments
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


import argparse


datas = {
	'carrés': {'%s' % x:(x+1)**2 for x in range(20)},
	'cube': {'%s' % x:(x+1)**3 for x in range(20)},
}

def test(namespace):
	return namespace

def available_keys(namespace):
	return list(datas.keys())

def get(namespace):
	return '%s:%s' % (
		datas['carrés'].get(namespace.value),
		datas['cube'].get(namespace.value))

def getParser():
	parser = argparse.ArgumentParser(
		prog='./testeur.py',
		description='''Testeur pour arguments''',
		epilog='''Exemple du chapitre 14'''
	)

	subparsers = parser.add_subparsers(help='commands')

	test_parser = subparsers.add_parser(
		'test',
		description='Test du parseur',
		help='Permet de tester le parseur',
	)
	test_parser.set_defaults(func=test)

	list_parser = subparsers.add_parser(
		'list',
		aliases=['l'],
		description='liste des données disponibles',
		help='Permet de récupérer la liste des fonctionnalités disponibles',
	)
	list_parser.set_defaults(func=available_keys)

	get_parser = subparsers.add_parser(
		'get',
		description='une valeur',
		help='Permet de donner toutes les valeurs relatives à l\'argument'
	)
	get_parser.add_argument(
		'value',
		help='valeur'
	)
	get_parser.set_defaults(func=get)

	return parser

if __name__ == "__main__":
	parser = getParser()
	args=parser.parse_args()
	print(args.func(args))


