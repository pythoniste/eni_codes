#!/usr/bin/python3
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
__email__ = "pythoniste@protonmail.com"
__status__ = "Production"


from itertools import cycle
from array import array
from time import time
import os


def infos() -> dict:
    """Empreinte mémoire du processus courant"""

    with open('/proc/%d/status' % os.getpid()) as t:
        v = t.read()
    return dict(
        [
            [b.strip() for b in a.split(':')]
            for a in v.splitlines()
        ]
    )


def memory() -> tuple[str, str, str, str]:
    """Renvoie des informations spécifiques parmi le dictionnaire d'information général"""
    i = infos()
    return i['VmSize'], i['VmStk'], i['VmData'], i['VmRSS']


def crible1(m: int) -> list:
    """Algorithme classique pour le crible d'Ératosthène"""
    res, n = [i for i in range(2, m+1)], 2
    while n:
        for i in res[res.index(n)+1:]:
            if i % n == 0:
                res.remove(i)
        if res.index(n) + 1 < len(res):
            n = res[res.index(n) + 1]
        else:
            return res


def crible2(m: int) -> list:
    """Algorithme pythonique pour le crible d'Ératosthène"""

    res = [i for i in range(m+1)]
    res[1], n = 0, 2
    while n**2 <= m:
        res[n*2::n], n = cycle([0]), n+1
        while not res[n]:
            n += 1
    return [i for i in res if i != 0]


def crible3(m: int) -> list:
    """Algorithme alternatif"""

    found, numbers, i = [], [], 2
    while i <= m:
        if i not in numbers:
            found.append(i)
            for j in range(i, m+1, i):
                numbers.append(j)
        i += 1
    return found


def crible4(m: int) -> list:
    """Algorithme alternatif"""

    if m < 2**31:
        t = 'i'
    else:
        if m >= 2**64:
            print('AVERTISSEMENT, le maximum a été limité à %s' % 2**64-1)
        t = 'L'
    l, n = array(t), 2
    l.extend([i for i in range(m+1)])
    while n**2 <= m:
        l[n*2::n], n = array(t, [0]*(m//n-1)), n+1
        while not l[n]:
            n += 1
    return [i for i in l if i != 0]


def test() -> dict[int, tuple[float, float, float, float]]:
    """Mise en évidence des performances des deux algorithmes"""

    data = {}
    # memos = {}
    for m in [10, 100, 1000, 10000]:
        # m0=memory()
        t0 = time()
        crible1(m)
        t1 = time()
        # m1=memory()
        t2 = time()
        crible2(m)
        t3 = time()
        # m2=memory()
        t4 = time()
        crible3(m)
        t5 = time()
        # m3=memory()
        t6 = time()
        crible4(m)
        t7 = time()
        # m4=memory()
        data[m] = (t1-t0, t3-t2, t5-t4, t7-t6)
        # memos[m] = (m0, m1, m2, m3, m4)
    return data  # , memos


if __name__ == "__main__":
    sep = '+---------+-----------+------------+----------+------------+------------+'
    title = 'Crible'.center(len(sep)-2).center(len(sep), '|')
    head = '| maximum | classique | pythonique | gain (%) | alternatif | alternatif |'
    body = '| %7d | %9.7f |  %9.7f | %8.2f |  %9.7f |  %9.7f |'
    memo = '| %7s | %9s |  %9s |          |  %9s |  %9s |'
    # datas, memos = test()
    datas = test()

    for s in [sep, title, sep, head]:
        print(s)

    keys = list(datas.keys())
    keys.sort()
    for k in keys:
        d = datas[k]
        d = (k,) + d[:2] + (100. * d[1] / d[0],) + d[2:]
        print(body % d)
        # for i, v in zip(('VmSize', 'VmStk', 'VmData', 'VmRSS'), memos[k]):
        #     i=(i,)+v
        #     print(memo % i)
        # print(sep)
    print(sep)
