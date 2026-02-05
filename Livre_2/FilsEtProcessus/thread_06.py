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


from threading import Thread, Condition

from time import sleep
from io import StringIO


class Consumer(Thread):
	def __init__(self, name, buffer, condition):
		self.buffer = buffer
		self.condition = condition
		self.current = ''
		Thread.__init__(self, name=name)
	def run(self):
		while True:
			self.condition.acquire()
			if self.buffer.getvalue() in ['', self.current]:
				print('Attente du consommateur %s' % self.getName())
				self.condition.wait()
			print('Reprise du consommateur %s' % self.getName())
			self.current = self.buffer.getvalue()
			if self.buffer.getvalue() == '#':
				print('Fin du consommateur %s' % self.getName())
				return
			print('Reçu %s < "%s"' % (self.getName(), self.current))
			self.condition.release()

class Producer(Thread):
	def __init__(self, buffer, condition, phrases):
		self.buffer = buffer
		self.condition = condition
		self.phrases = phrases
		Thread.__init__(self)
	def run(self):
		self.phrases.append('#')
		for phrase in phrases:
			self.condition.acquire()
			self.buffer.seek(0)
			self.buffer.truncate(0)
			self.buffer.write(phrase)
			print('Envoyé > "%s"' % phrase)
			self.condition.notifyAll()
			sleep(0.000001)
			self.condition.release()
		print('Fin du producteur')

phrases = [
	"Phrase 1",
	"Phrase 2",
	"Phrase 3",
]

try:
	buffer = StringIO()
	condition = Condition()
	c1 = Consumer('1', buffer, condition)
	c2 = Consumer('2', buffer, condition)
	p = Producer(buffer, condition, phrases)
	c1.start()
	sleep(0.000001)
	c2.start()
	sleep(0.000001)
	p.start()
except:
	print("Error: unable to start thread")

