#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Exemple de création d'une plaquette PDF.
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
from reportlab.platypus.doctemplate import BaseDocTemplate
from reportlab.lib import colors


class PlaquetteTemplate (PageTemplate):
    """Modèle de Pages PDF pour une plaquette commerciale"""
    def __init__ (self, context):
        self.context = context
        self.largeur = self.context.document.pagesize[0]
        self.hauteur = self.context.document.pagesize[1]
        self.zone1 = Frame (0.7*cm, 13*cm, self.largeur - 0.7*cm, 10*cm)
        self.zone2 = Frame (0.7*cm, 9*cm, self.largeur - 0.7*cm, 6*cm)
        self.zone3 = Frame (0.7*cm, 5*cm, self.largeur - 0.7*cm, 2*cm)
        PageTemplate.__init__ (self, id="Tiers", frames=[self.zone1, self.zone2, self.zone3], pagesize=A4)
    def beforeDrawPage (self, canvas, doc):
        canvas.saveState ()
        try:
            self.zone1.addFromList( self.context.flowables_zone1 , canvas)
            self.zone2.addFromList( self.context.flowables_zone2 , canvas)
            self.zone3.addFromList( self.context.flowables_zone3 , canvas)
        finally:
            canvas.restoreState ()
    def afterDrawPage (self, canvas, doc):
        canvas.saveState ()
        try:
            canvas.setFillColorRGB(*colors.mediumaquamarine.rgba())
            canvas.setStrokeColorRGB(*colors.midnightblue.rgba())
            canvas.rect(0.7*cm, self.hauteur - 2*0.7*cm, 0.7*cm, 0.7*cm, fill=1)
        finally:
            canvas.restoreState ()

class PlaquettePDF:
	def __init__ (self, context):
		self.context = context
		self.built = 0
		self.objects = [Spacer (0, 0.5*cm)]
		self.styles = getSampleStyleSheet() 
		self.flowables_zone1=[Paragraph("ZONE 1", self.styles['Normal'])]
		self.flowables_zone2=[Paragraph("ZONE 2", self.styles['Normal'])]
		self.flowables_zone3=[Paragraph("ZONE 3", self.styles['Normal'])]
		self.document = BaseDocTemplate ("plaquette.pdf", leftMargin=0.7*cm, rightMargin=0.7*cm, topMargin=0.7*cm, bottomMargin=0.7*cm, pagesize=A4)
		self.document.addPageTemplates ( PlaquetteTemplate (self))
		self.document.build (self.objects)
		self.built = 1

PlaquettePDF('')

