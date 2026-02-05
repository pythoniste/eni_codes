#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Illustration de la création d'un template pour un fichier PDF.
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


from reportlab.platypus.doctemplate import PageTemplate
from reportlab.platypus.frames import Frame
from reportlab.lib.units import cm


class FlowTemplate (PageTemplate):
	"""Template for a pdf with datas in a flow."""
	def __init__ (self, parent):
		"""Initialization of Template : llc = lower left corner"""
		self.parent = parent
		self.largeur = self.parent.document.pagesize[0]
		self.hauteur = self.parent.document.pagesize[1]
		self.marginx, self.marginy = 0.7 * cm, 1.4 * cm
		self.llcx = self.largeur - self.marginx
		self.llcy = 1.0 * cm
		self.page = 0
		content = Frame (self.marginx, self.marginy, self.largeur - 2 * self.marginx, self.hauteur - 2 * self.marginy)
		PageTemplate.__init__ (self, "Content", [content])
	def beforeDrawPage (self, canvas, doc):
		"""before Drawing Page, we draw elements of the template"""
		canvas.saveState ()
		try:
			self.drawTemplate(canvas, doc)
		finally:
			canvas.restoreState()
	def drawTemplate(self, canvas, doc):
		"""Can be overridden"""
		self.page += 1
		#Dessin d'un carré noir 
		canvas.setFillColorCMYK( 0, 0, 0, 1 )
		#canvas.setStrokeColorCMYK( 0, 0, 0, 1 )
		canvas.rect(self.llcx, self.llcy, 0.4 * cm, 0.4 * cm, stroke=0, fill=1 )
		#Ajout du numéro de la page dans le carré noir.
		canvas.setFont ('Helvetica', 8)
		canvas.setFillColorCMYK( 0, 0, 0, 0 )
		if self.page >= 10:
			canvas.drawRightString (self.llcx + 0.35 * cm, self.llcy + 0.1 * cm, "%d" % self.page)
		else:
			canvas.drawRightString (self.llcx + 0.3 * cm, self.llcy + 0.1 * cm, "%d" % self.page)

