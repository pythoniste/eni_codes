#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Exemple de serveur REST
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


from bottle import route, run


if __name__ == "__main__":
	@route('hello/:name', method='GET')
	def get_set_of_results(name):
		return {'message': 'Hello %s' % name}
	run(port=8095)

