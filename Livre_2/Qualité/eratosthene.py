#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Implémentations du crible d'Ératosthène
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


from array import array
from timeit import timeit
import cProfile, pstats
from io import StringIO
from time import time
import os
import dis

#def infos():
#    """Empreinte mémoire du processus courant"""
#    t=open('/proc/%d/status' % os.getpid())
#    v=t.read()
#    t.close()
#    return dict([[b.strip() for b in a.split(':')] for a in v.splitlines()])
#
#def memory():
#    i=infos()
#    return i['VmSize'], i['VmStk'], i['VmData'], i['VmRSS']

def crible1(m):
    """Algorithme classique pour le crible d'Ératosthène"""
    l, n = [i for i in range(2, m+1)], 2
    while n:
        for i in l[l.index(n)+1:]:
            if i % n == 0:
                l.remove(i)
        if l.index(n) +1 < len(l):
            n = l[l.index(n) + 1]
        else:
            return l

def crible2(m):
    """Algorithme pythonique pour le crible d'Ératosthène"""
    l = [i for i in range(m+1)]
    l[1], n = 0, 2
    while n**2 <= m:
        l[n*2::n], n = [0] * (int(m/n) -1), n+1
        while not l[n]: n+= 1
    return [i for i in l if i != 0]

def crible3(m):
    """Algorithme alternatif"""
    found, numbers, i = [], [], 2
    while (i <= m):
        if  i not in numbers:
            found.append(i)
            for j in range(i, m+1, i):
                numbers.append(j)
        i += 1
    return found

def crible4(m):
    """Algorithme alternatif"""
    if m < 2**31:
        t = 'i'
    else:
        if m>= 2**64:
            print('AVERTISSEMENT, le maximum a été limité à %s' % 2**64-1)
        t = 'L'
    l, n = array(t), 2
    l.extend([i for i in range(m+1)])
    while n**2 <= m:
        l[n*2::n], n = array(t, [0]*(m//n-1)), n+1
        while not l[n]: n+= 1
    return [i for i in l if i != 0]

def tester(callback, *values, **kvalues):
    pr = cProfile.Profile()
    pr.enable()
    callback(*values, **kvalues)
    pr.disable()
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    return s.getvalue()

def test():
    """Mise en évidence des performances des deux algorithmes"""
    for i in range(1, 5):
        print('Crible%s pour 1000 entiers: ' % i, sep="")
        print(timeit('crible%s(1000)' % i, number=10, setup="from __main__ import crible%s" % i))
        print('---')
        print(tester(eval('crible%s' % i), 1000))

if __name__ == '__main__':
    test()
