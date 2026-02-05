#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Définition d'une liste d'objets uniques et quelques tests unitaires.
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "pythoniste@protonmail.com"
__status__ = "Production"


import unittest
from typing import Self, Any


class UniqueList(list):
    """Liste d'objets uniques"""

    def __init__(self, seq: list[Any] | None = None) -> None:
        """Surcharge générique du constructeur"""

        if seq is None:
            seq = []

        list.__init__(self, [])

        for value in seq:
            self.append(value)

    def append(self, value: Any) -> None:
        """Surcharge de la méthode d'ajout d'éléments en fin de liste"""

        if value not in self:
            list.append(self, value)

    def insert(self, index: int, value: Any) -> None:
        """Surcharge de la méthode d'ajout d'éléments à un index donné"""

        if value not in self:
            list.insert(self, index, value)

    def extend(self, seq: list[Any]) -> None:
        """Surcharge de la méthode de modification de plusieurs éléments"""

        for value in seq:
            self.append(value)

    def __setitem__(self, index: int, value: Any) -> None:
        """Surcharge de la méthode de modification d'un élément"""

        if value not in self:
            list.__setitem__(self, index, value)

    def __add__(self, seq: list[Any]) -> Self:
        """Surcharge de la méthode d'ajout de plusieurs éléments"""

        return UniqueList(list(self) + list(seq))

    def __iadd__(self, seq: list[Any]) -> Self:
        """Surcharge de la méthode d'ajout de plusieurs éléments"""

        for value in seq:
            self.append(value)
        return self


class UniqueListTest(unittest.TestCase):
    """Test des listes d'éléments uniques"""

    def test_construction(self) -> None:
        """Testing `__init__` method of UniqueList"""

        self.test = UniqueList([1, 2])
        self.assertEqual(self.test, [1, 2])
        self.test = UniqueList([3, 4, 3])
        self.assertEqual(self.test, [3, 4])

    def test_append(self) -> None:
        """Testing `append` method of UniqueList"""

        self.test = UniqueList()
        self.test.append(5)
        self.assertEqual(self.test, [5])
        self.test.append(6)
        self.assertEqual(self.test, [5, 6])
        self.test.append(6)
        self.assertEqual(self.test, [5, 6])

    def test_insert(self) -> None:
        """Testing `insert` method of UniqueList"""

        self.test = UniqueList()
        self.test.insert(0, 5)
        self.assertEqual(self.test, [5])
        self.test.insert(1, 6)
        self.assertEqual(self.test, [5, 6])
        self.test.insert(0, 6)
        self.assertEqual(self.test, [5, 6])

    def test_extend(self) -> None:
        """Testing `extend` method of UniqueList"""

        self.test = UniqueList()
        self.test.extend([5, 7, 9])
        self.assertEqual(self.test, [5, 7, 9])
        self.test = UniqueList()
        self.test.extend([5, 7, 5, 9])
        self.assertEqual(self.test, [5, 7, 9])
        self.test = UniqueList([1])
        self.test.extend([5, 7, 9])
        self.assertEqual(self.test, [1, 5, 7, 9])
        self.test = UniqueList([1])
        self.test.extend([5, 7, 1, 9])
        self.assertEqual(self.test, [1, 5, 7, 9])

    def test_set_item(self) -> None:
        """Testing `__set_item__` method of UniqueList"""

        self.test = UniqueList([5, 6])
        self.assertEqual(self.test, [5, 6])
        self.test[0] = 1
        self.assertEqual(self.test, [1, 6])
        self.test[0] = 6
        self.assertEqual(self.test, [1, 6])

    def test_add(self) -> None:
        """Testing `__add__` method of UniqueList"""

        self.test = UniqueList()
        test = self.test + [5, 7, 9]
        self.assertEqual(test, [5, 7, 9])
        self.test = UniqueList()
        test = self.test + [5, 7, 5, 9]
        self.assertEqual(test, [5, 7, 9])
        self.test = UniqueList([1])
        test = self.test + [5, 7, 9]
        self.assertEqual(test, [1, 5, 7, 9])
        self.test = UniqueList([1])
        test = self.test + [5, 7, 1, 9]
        self.assertEqual(test, [1, 5, 7, 9])

    def test_iadd(self) -> None:
        """Testing `__iadd__` method of UniqueList"""

        self.test = UniqueList()
        self.test += [5, 7, 9]
        self.assertEqual(self.test, [5, 7, 9])
        self.test = UniqueList()
        self.test += [5, 7, 5, 9]
        self.assertEqual(self.test, [5, 7, 9])
        self.test = UniqueList([1])
        self.test += [5, 7, 9]
        self.assertEqual(self.test, [1, 5, 7, 9])
        self.test = UniqueList([1])
        self.test += [5, 7, 1, 9]
        self.assertEqual(self.test, [1, 5, 7, 9])


if __name__ == "__main__":
    unittest.main()
