#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de création d'un "démon" au sens UNIX du terme
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


import os
import time
import sys

pid=os.fork()
if pid==0:
    for i in range(60):
        print('Je suis le fils PID: %s et je tourne. Mon père est PID %s' % (os.getpid(), os.getppid()))
        time.sleep(1)
else:
    print('Je suis le père PID: %s, mon fils est le PID %s' % (os.getpid(), pid))
    time.sleep(5)
    sys.exit(0)

