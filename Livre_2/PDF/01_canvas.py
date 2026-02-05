#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Illustration de l'utilisation du canvas pour la génération de PDF.
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm


canvas = Canvas("hello.pdf")
canvas.setTitle("Premier document")
canvas.setSubject("Creation de document PDF avec ReportLab")
canvas.setAuthor('SCH')
canvas.setKeywords(['PDF', 'ReportLab', 'Python'])
canvas.setCreator('sch')
canvas.setFont("Helvetica", 36)
canvas.drawCentredString(12.0 * cm, 18.0 * cm, "Hello world")
canvas.setFont("Times-Roman", 12)
canvas.drawString(1.0 * cm, 1.0 * cm, "O")
canvas.drawString(2.0 * cm, 1.0 * cm, "X")
canvas.drawString(1.0 * cm, 2.0 * cm, "Y")
canvas.drawString(8.5 * cm, 16.0 * cm, "G")
canvas.drawRightString(8.5 * cm, 15.0 * cm, "D")
canvas.drawCentredString(8.5 * cm, 14.0 * cm, "C")
canvas.drawString(12.5 * cm, 16.0 * cm, "Aligné à gauche")
canvas.drawRightString(12.5 * cm, 15.0 * cm, "Aligné à droite")
canvas.drawCentredString(12.5 * cm, 14.0 * cm, "Aligné au centre")
canvas.drawCentredString(10.5 * cm, 10.0 * cm, '\n'.join(["Aligné plein centre"] * 5))
canvas.drawString(18.5 * cm, 12.0 * cm, "Mal Aligné" * 5)
canvas.drawRightString(2.5 * cm, 12.0 * cm, "Mal Aligné" * 5)
canvas.save()

