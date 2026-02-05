#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple d'utilisation de la bibliothèque PIL
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"



from PIL import Image
import os.path


def resize(filename, formats={600: 'screen', 150: 'thumbnail'}):
	# Initialisation
	file, ext = os.path.splitext(filename)
	im = Image.open(filename)
	w, h = im.size
	# Redimensionnement
	for s in sorted(formats, reverse=True):
		im.thumbnail((s, int(1.*s*h/w)), Image.ANTIALIAS)
		im.save('%s_%s.png' % (file, formats[s]), 'PNG')


def rotate(filename, angles):
	file, ext = os.path.splitext(filename)
	im = Image.open(filename)
	for angle in angles:
		im2 = im.rotate(angle)
		im2.save('original_thumbnail_%s.png' % angle, 'PNG')


if __name__ == '__main__':
	resize('original.png')
	rotate('original_thumbnail.png', [10, 30, 45, 90, 180])


