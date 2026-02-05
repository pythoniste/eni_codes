#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Script d'illustration travaillant sur les nombres premiers de Mersenne.
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "pythoniste@protonmail.com"
__status__ = "Production"


from sys import stdout
from math import sqrt, log
from time import time


def is_prime(p: int) -> bool:
    """Test de primalité de Lucas-Lehmer"""

    if p == 2:
        return True
    elif p <= 1 or p % 2 == 0:
        return False
    for i in range(3, int(sqrt(p))+1, 2):
        if p % i == 0:
            return False
    return True


def is_mersenne_prime(p: int) -> bool:
    """Test de primalité de Lucas-Lehmer"""

    if p == 2:
        return True
    m_p = (1 << p) - 1
    s = 4
    for i in range(3, p + 1):
        s = (s ** 2 - 2) % m_p
    return s == 0


t0 = time()
precision = 20000
long_bits_width = precision * log(10, 2)
upb_prime = int(long_bits_width - 1) // 2
upb_count = 45

print(f"Recherche des nombres premiers de Mersenne pour M compris entre 2 et {upb_prime:d}:")

count = 0

for number in range(2, upb_prime+1):
    if is_prime(number) and is_mersenne_prime(number):
        print(f"M{number:d}", end=" ")
        stdout.flush()
        count += 1
    if count >= upb_count:
        break

print("Temps d'exécution : %.2f" % (time() - t0))
