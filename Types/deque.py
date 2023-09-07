#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Voici un exemple d'utilisation depuis un terminal bash:

    $ ./test_deque.py
    listes : 0.0000250340
    deque1 : 0.0000128746
    deque2 : 0.0000071526
    ---------------------
    listes : 0.0015981197
    deque1 : 0.0004830360
    deque2 : 0.0004899502
    ---------------------
    listes : 0.0490779877
    deque1 : 0.0033481121
    deque2 : 0.0033009052

    Voici le même exemple depuis une console Python :
    (les valeurs seront différentes entre chaque lancement, mais les ordres de grandeur devraient être cohérents)

    >>> main()
    listes : 0.0000250340
    deque1 : 0.0000128746
    deque2 : 0.0000071526
    ---------------------
    listes : 0.0015981197
    deque1 : 0.0004830360
    deque2 : 0.0004899502
    ---------------------
    listes : 0.0490779877
    deque1 : 0.0033481121
    deque2 : 0.0033009052

"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "pythoniste@protonmail.com"
__status__ = "Production"


from collections import deque
from time import time


def test1() -> None:
    """Cas d'utilisation classique pour un tampon
    (FIFO, premier arrivé = premier parti)

    On utilise simplement une liste
    """
    tested_instance = []
    tested_instance.insert(0, 1)
    tested_instance.insert(0, 2)
    tested_instance.pop()
    tested_instance.insert(0, 3)
    tested_instance.insert(0, 4)
    tested_instance.pop()
    tested_instance.pop()
    tested_instance.insert(0, 5)
    tested_instance.pop()
    tested_instance.pop()


def test2() -> None:
    """Cas d'utilisation classique pour un tampon
    (FIFO, premier arrivé = premier parti)

    On utilise l'objet deque en le remplissant par la droite
    et en le vidant par la gauche
    """
    tested_instance = deque()
    tested_instance.append(1)
    tested_instance.append(2)
    tested_instance.popleft()
    tested_instance.append(3)
    tested_instance.append(4)
    tested_instance.popleft()
    tested_instance.popleft()
    tested_instance.append(5)
    tested_instance.popleft()
    tested_instance.popleft()


def test3() -> None:
    """Cas d'utilisation classique pour un tampon
    (FIFO, premier arrivé = premier parti)

    On utilise l'objet deque en le remplissant par la gauche
    et en le vidant par la droite
    """
    tested_instance = deque()
    tested_instance.appendleft(1)
    tested_instance.appendleft(2)
    tested_instance.pop()
    tested_instance.appendleft(3)
    tested_instance.appendleft(4)
    tested_instance.pop()
    tested_instance.pop()
    tested_instance.appendleft(5)
    tested_instance.pop()
    tested_instance.pop()


def test11() -> None:
    """Cas d'utilisation d'un tampon qui est d'abord rempli puis vidé
    (FIFO, premier arrivé = premier parti)

    On utilise simplement une liste
    """
    tested_instance = []
    for i in range(1000):
        tested_instance.insert(0, i)
    for i in range(1000):
        tested_instance.pop()


def test12() -> None:
    """Cas d'utilisation d'un tampon qui est d'abord rempli puis vidé
    (FIFO, premier arrivé = premier parti)

    On utilise l'objet deque en le remplissant par la droite
    et en le vidant par la gauche
    """
    tested_instance = deque()
    for i in range(1000):
        tested_instance.append(i)
    for i in range(1000):
        tested_instance.popleft()


def test13() -> None:
    """Cas d'utilisation d'un tampon qui est d'abord rempli puis vidé
    (FIFO, premier arrivé = premier parti)

    On utilise l'objet deque en le remplissant par la gauche
    et en le vidant par la droite
    """
    tested_instance = deque()
    for i in range(1000):
        tested_instance.appendleft(i)
    for i in range(1000):
        tested_instance.pop()


def test21() -> None:
    """Cas d'utilisation intermédiaire
    (FIFO, premier arrivé = premier parti)

    On utilise simplement une liste
    """
    tested_instance = []
    for j in range(10):
        for i in range(1000):
            tested_instance.insert(0, i)
        for i in range(500):
            tested_instance.pop()
    for j in range(10):
        for i in range(500):
            tested_instance.insert(0, i)
        for i in range(1000):
            tested_instance.pop()


def test22() -> None:
    """Cas d'utilisation intermédiaire d'un tampon
    (FIFO, premier arrivé = premier parti)

    On utilise l'objet deque en le remplissant par la droite
    et en le vidant par la gauche
    """
    tested_instance = deque()
    for j in range(10):
        for i in range(1000):
            tested_instance.append(i)
        for i in range(500):
            tested_instance.popleft()
    for j in range(10):
        for i in range(500):
            tested_instance.append(i)
        for i in range(1000):
            tested_instance.popleft()


def test23() -> None:
    """Cas d'utilisation intermédiaire d'un tampon
    (FIFO, premier arrivé = premier parti)

    On utilise l'objet deque en le remplissant par la gauche
    et en le vidant par la droite
    """
    tested_instance = deque()
    for j in range(10):
        for i in range(1000):
            tested_instance.appendleft(i)
        for i in range(500):
            tested_instance.pop()
    for j in range(10):
        for i in range(500):
            tested_instance.appendleft(i)
        for i in range(1000):
            tested_instance.pop()


def main() -> None:
    """Lancement des tests et affichage des résultats"""
    t0 = time()
    test1()
    t1 = time()
	test2()
	t2 = time()
	test3()
	t3 = time()
	print('listes : %.10f' % (t1-t0))
	print('deque1 : %.10f' % (t2-t1))
	print('deque2 : %.10f' % (t3-t2))
	t0 = time()
	test11()
	t1 = time()
	test12()
	t2 = time()
	test13()
	t3 = time()
	print('---------------------')
	print('listes : %.10f' % (t1-t0))
	print('deque1 : %.10f' % (t2-t1))
	print('deque2 : %.10f' % (t3-t2))
	t0 = time()
	test21()
	t1 = time()
	test22()
	t2 = time()
	test23()
	t3 = time()
	print('---------------------')
	print('listes : %.10f' % (t1-t0))
	print('deque1 : %.10f' % (t2-t1))
	print('deque2 : %.10f' % (t3-t2))


if __name__ == "__main__":
	main()
