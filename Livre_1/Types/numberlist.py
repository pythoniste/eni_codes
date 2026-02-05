#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Définition d'une liste d'entiers et quelques tests unitaires.
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "pythoniste@protonmail.com"
__status__ = "Production"


from typing import Self
import unittest


class NumberList(list):
    """Liste de nombres"""

    __types__ = [type(0), type(0.)]

    def __init__(self, seq: list[int | float] | None = None) -> None:
        """Surcharge générique du constructeur"""

        if seq is None:
            seq = []

        for index, value in enumerate(seq):
            if type(value) not in self.__types__:
                raise TypeError("l'objet %s d'index %s de la séquence n'est pas un nombre" % (value, index))
        list.__init__(self, seq)

    def append(self, value: int | float) -> None:
        """Surcharge de la méthode d'ajout d'éléments en fin de liste"""
        if type(value) not in self.__types__:
            raise TypeError("%s n'est pas un nombre" % value)
        list.append(self, value)

    def insert(self, index: int, value: int | float) -> None:
        """Surcharge de la méthode d'ajout d'éléments à un index donné"""
        if type(value) not in self.__types__:
            raise TypeError("%s n'est pas un nombre" % value)
        list.insert(self, index, value)

    def extend(self, seq: list[int | float]) -> None:
        """Surcharge de la méthode de modification de plusieurs éléments"""

        for index, value in enumerate(seq):
            if type(value) not in self.__types__:
                raise TypeError("l'objet %s d'index %s de la séquence n'est pas un nombre" % (value, index))
        list.extend(self, seq)

    def __setitem__(self, index: int, value: int | float) -> None:
        """Surcharge de la méthode de modification d'un élément"""
        if type(value) not in self.__types__:
            raise TypeError("%s n'est pas un nombre" % value)
        list.__setitem__(self, index, value)

    def __add__(self, seq: list[int | float]) -> Self:
        """Surcharge de la méthode d'ajout de plusieurs éléments"""

        for index, value in enumerate(seq):
            if type(value) not in self.__types__:
                raise TypeError("l'objet %s d'index %s de la séquence n'est pas un nombre" % (value, index))
        return list.__add__(self, seq)

    def __iadd__(self, seq: list[int | float]) -> Self:
        """Surcharge de la méthode d'ajout de plusieurs éléments"""

        for index, value in enumerate(seq):
            if type(value) not in self.__types__:
                raise TypeError("l'objet %s d'index %s de la séquence n'est pas un nombre" % (value, index))
        list.__iadd__(self, seq)
        return self


class NumberListTest(unittest.TestCase):
    """Test des listes de nombres"""

    def test_construction(self) -> None:
        """Test the construction of a NumberList instance"""

        self.test = NumberList([1, 2.])
        self.assertEqual(self.test, [1, 2.])
        self.assertRaises(TypeError, NumberList, ['7'])

    def test_append(self) -> None:
        """Test the `append` method of a NumberList instance"""

        self.test = NumberList()
        self.test.append(5)
        self.assertEqual(self.test, [5])
        self.test.append(6.)
        self.assertEqual(self.test, [5, 6.])
        self.assertRaises(TypeError, self.test.append, '7')

    def test_insert(self) -> None:
        """Test the `insert` method of a NumberList instance"""

        self.test = NumberList()
        self.test.insert(0, 5)
        self.assertEqual(self.test, [5])
        self.test.insert(1, 6.)
        self.assertEqual(self.test, [5, 6.])
        self.assertRaises(TypeError, self.test.append, '7')

    def test_extend(self) -> None:
        """Test the `extend` method of a NumberList instance"""

        self.test = NumberList()
        self.test.extend([5, 7, 9.])
        self.assertEqual(self.test, [5, 7, 9.])
        self.assertRaises(TypeError, self.test.extend, [5, '7', 9.])
        self.assertEqual(self.test, [5, 7, 9.])

    def test_set_item(self) -> None:
        """Test the `__setitem__` method of a NumberList instance"""
        self.test = NumberList([5])
        self.assertEqual(self.test, [5])
        self.test[0] = 1
        self.assertEqual(self.test, [1])
        self.assertRaises(TypeError, self.test.__setitem__, 0, '7')

    def test_add(self) -> None:
        """Test the `__add__` method of a NumberList instance"""
        self.test = NumberList()
        test = self.test + [5, 7, 9.]
        self.assertEqual(test, [5, 7, 9.])
        self.assertRaises(TypeError, self.test.__add__, [5, '7', 9.])
        self.assertEqual(self.test, [])

    def test_iadd(self) -> None:
        """Test the `__iadd__` method of a NumberList instance"""
        self.test = NumberList()
        self.test += [5, 7, 9.]
        self.assertEqual(self.test, [5, 7, 9.])
        self.assertRaises(TypeError, self.test.__iadd__, [5, '7', 9.])
        self.assertEqual(self.test, [5, 7, 9.])


if __name__ == "__main__":
    unittest.main()
