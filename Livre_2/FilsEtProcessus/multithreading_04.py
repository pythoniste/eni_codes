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


from multiprocessing import Process, Lock

import sys


def work(name, lock):
	with lock:
		print('Work with %s' % name)
		sys.stdout.flush()

lock = Lock()
for i in range(10):
	Process(target=work, args=(i, lock)).start()

print('GO')

