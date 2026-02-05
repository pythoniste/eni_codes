#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Illustration du fonctionnement bas niveau des threads
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


from threading import Thread
from time import time, ctime, sleep


class Worker(Thread):
	def __init__(self, name, delay):
		self.delay = delay
		Thread.__init__(self, name=name)
	def run(self):
		for i in range(5):
			print("%s: Appel %s, %s" % (self.getName(), i, ctime(time())))
			sleep(self.delay)

try:
	t1 = Worker("T1", 2)
	t2 = Worker("T2", 3)
	t1.start()
	t2.start()
except:
	print("Error: unable to start threads")

