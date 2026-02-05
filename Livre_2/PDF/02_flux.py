#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Illustration de l'écriture d'un flux de données dans un fichier PDF.
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet 
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Image
from reportlab.platypus import PageBreak
from reportlab.platypus import Table


styles = getSampleStyleSheet() 
mon_style = ParagraphStyle(name='mon_style', alignment=TA_JUSTIFY, fontName = "Helvetica", fontSize = 14)
styles.add(mon_style)
style_tableau = [
    ('ALIGN',         (0,0),  (-1,-1), "LEFT"),
    ('VALIGN',        (0,0),  (-1,-1), "TOP"),
    ('LEFTPADDING',   (0,0),  (-1,-1), 0*cm),
    ('RIGHTPADDING',  (0,0),  (-1,-1), 0*cm),
    ('TOPPADDING',    (0,0),  (-1,-1), 0*cm),
    ('BOTTOMPADDING', (0,0),  (-1,-1), 0*cm),
]
style_tableau1 = style_tableau[:]
style_tableau1.append(('LINEABOVE', (0,0), (-1, 0), 1, colors.turquoise))
style_tableau1.append(('LINEABOVE', (0,1), (-1,-1), 0.5, colors.darkturquoise))

flowables = []
flowables.append(Paragraph("Fichier PDF Généré", styles["Heading1"]))
flowables.append(Paragraph("Sébastien CHAZALLET", styles["Normal"]))
flowables.append(Paragraph("http://www.inspyration.com", styles["Code"]))
content = """Ce document est généré par le script 02_flux.py.
Ce script est livré avec le présent ouvrage.
Vous pouvez le modifier à souhait pour faire vos propres expériences"""
flowables.append(Paragraph(content, styles["Normal"]))

flowables.append(Spacer (0, 0.2*cm))

flowables.append(Image('hello.pdf.png', height = 5 * cm, width = 8 * cm))

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart

drawing = Drawing(10 * cm, 5 * cm)
lc = HorizontalLineChart()
lc.data = [
	(0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1000),
	(0, 64, 128, 192, 256, 320, 384, 448, 512, 576, 640, 704),
]
legend = ["Jan", "Fev", "Mar", "Avr", "Mai", "Jun", "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"]
lc.categoryAxis.categoryNames = legend
lc.valueAxis.valueMin = 0
lc.valueAxis.valueMax = 1000
lc.valueAxis.valueStep = 200
lc.lines[0].strokeWidth = 2
lc.lines[1].strokeWidth = 1.5
drawing.add(lc)
flowables.append(drawing)

flowables.append(PageBreak())

data = []
line = []
line.append( Paragraph ("Technologie", styles["Normal"]) )
line.append( Paragraph ("Logiciel", styles["Normal"]) )
line.append( Paragraph ("Alternatives", styles["Normal"]) )
data.append(line)
line = []
line.append( Paragraph ("Système d'exploitation", styles["Normal"]) )
line.append( Paragraph ("Debian", styles["Normal"]) )
line.append( Paragraph ("Ubuntu, Fedora", styles["Normal"]) )
data.append(line)
line = []
line.append( Paragraph ("Serveur d'annuaires", styles["Normal"]) )
line.append( Paragraph ("openLDAP", styles["Normal"]) )
line.append( Paragraph ("...", styles["Normal"]) )
data.append(line)
line = []
line.append( Paragraph ("Serveur web", styles["Normal"]) )
line.append( Paragraph ("Apache2", styles["Normal"]) )
line.append( Paragraph ("LightHttpd", styles["Normal"]) )
data.append(line)
flowables.append(Table(data, colWidths=[5*cm, 5*cm, 8*cm], style=style_tableau1))

pdf = SimpleDocTemplate('test.pdf', pagesize = A4, title = 'Premier test', author = 'SCH')
pdf.build(flowables)

