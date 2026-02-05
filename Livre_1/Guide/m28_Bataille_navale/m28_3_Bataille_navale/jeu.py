import sys

from itertools import product, repeat
from random import choice

from saisie import (
    demander_saisie_oui_ou_non,
    demander_saisie_case,
)


LONGUEURS_BATEAUX = [2, 3, 3, 4, 4, 5]
ORDINAL = 0x2680

CASE_NON_JOUE = chr(0x2610)
CASE_TOUCHE = chr(0x2611)
CASE_BLANC = chr(0x2612)

HORIZONTAL = 0
VERTICAL = 1

ORIENTATIONS = (VERTICAL, HORIZONTAL)


class Conventions:
    """Classe contenant des attributs et des méthodes statiques"""

    plateau_nb_lignes = 10
    plateau_nb_colonnes = 10

    navires_longueur = [2, 3, 3, 4, 4, 5]

    @staticmethod
    def generer_nom_ligne(x):
        return chr(65 + x)

    @staticmethod
    def generer_nom_colonne(y):
        return str(y)

    @staticmethod
    def generer_nom_case(x, y):
        return Conventions.generer_nom_ligne(x) +\
               Conventions.generer_nom_colonne(y)


class Case:
    instances = {}
    jouees = set()

    def __init__(self, plateau, x, y):
        # Aggrégation du plateau
        self.plateau = plateau

        # Aggrégation des coordonnées
        self.x = x
        self.y = y
        # On souhaite pouvoir accéder à une case à partir de ses coordonnées
        Case.instances[x, y] = self

        # Génération du nom de la case
        self._generer_nom()
        # On souhaite pouvoir accéder à une case à partir de son nom
        Case.instances[self.nom] = self

        # Suivi de l'évolution de la case
        self.jouee = False
        self.navire = None  # Non reliée à un navire pour l'instant.

    def _generer_nom(self):
        """Cette méthode peut être surchargée facilement"""
        self.nom = Conventions.generer_nom_case(self.x, self.y)

    def jouer(self):
        """décrit ce qu'il se passe lorsque l'on joue une case"""
        self.jouee = True
        self.jouees.add(self)

        if self.navire is not None:
            if len(self.navire.cases - self.plateau.cases_jouees) == 0:
                print("Coulé !!")
            else:
                print("Touché !")
        else:
            print("Dans l'eau !")

    @classmethod
    def generer_cases(cls, plateau):
        for x, y in product(range(Conventions.plateau_nb_lignes),
                            range(Conventions.plateau_nb_colonnes)):
            Case(plateau, x, y)

    def __str__(self):
        """Surcharge de la méthode de transformation en chaîne"""
        if not self.jouee:
            return CASE_NON_JOUE
        elif self.navire is None:
            return CASE_BLANC
        return CASE_TOUCHE


class Navire:
    instances = []
    cases_occupees = set()

    def __init__(self, plateau, longueur):
        self.plateau = plateau
        self.longueur = longueur
        self.orientation = choice(ORIENTATIONS)
        self.touche = False
        self.coule = False

        # performance / lisibilité:
        nb_lignes = Conventions.plateau_nb_lignes
        nb_colonnes = Conventions.plateau_nb_colonnes
        nb2l = Conventions.generer_nom_ligne
        nb2c = Conventions.generer_nom_colonne

        while True:
            if self.orientation == HORIZONTAL:
                rang = choice(range(nb_lignes))
                premier = choice(range(nb_colonnes + 1 - longueur))
                lettre = nb2l(rang)
                chiffres = [nb2c(x) for x in range(premier, premier + longueur)]
                self.cases = {Case.instances[ligne + colonne]
                              for ligne, colonne in product(repeat(lettre, longueur), chiffres)}
            else:
                rang = choice(range(nb_colonnes))
                premier = choice(range(nb_lignes + 1 - longueur))
                chiffre = nb2c(rang)
                lettres = [nb2l(x) for x in range(premier, premier + longueur)]
                # Créer le navire
                self.cases = {Case.instances[ligne + colonne]
                              for ligne, colonne in product(lettres, repeat(chiffre, longueur))}

            for existant in Navire.instances:
                if self.cases.intersection(existant.cases):
                    # Une case du navire se recoupe avec un navire existant
                    # La navire n'est pas bien placé, on le replace
                    break  # break relatif au "for existant in navires:"
            else:
                # Ajouter le navire au conteneur de navires
                Navire.instances.append(self)
                # Informer la case qu'elle contient un navire.
                for case in self.cases:
                    case.navire = self
                # Rajouter ces cases aux cases occupees :
                Navire.cases_occupees |= self.cases
                break  # break relatif au "while True:"

    @classmethod
    def generer_navires(cls, plateau):
        for longueur in Conventions.navires_longueur:
            Navire(plateau, longueur)


class Plateau:

    def __init__(self):
        # On crée les cases:
        Case.generer_cases(self)

        # On crée les navires:
        Navire.generer_navires(self)

        # performance / lisibilité:
        nb_lignes = Conventions.plateau_nb_lignes
        nb_colonnes = Conventions.plateau_nb_colonnes
        nb2l = Conventions.generer_nom_ligne
        nb2c = Conventions.generer_nom_colonne

        # On crée l'utile pour pouvoir suivre la situation
        self.cases_jouees = set()

        # On génère ici les labels pour faciliter l'affichage
        self.label_lignes = [nb2l(x) for x in range(nb_lignes)]
        self.label_colonnes = [nb2c(x) for x in range(nb_colonnes)]

    trait_horizontal = " --" + "+---" * 10 + "+"

    def afficher(self):
        print("   |", " | ".join(self.label_colonnes), "|")

        iter_label_lignes = iter(self.label_lignes)

        for x, y in product(range(Conventions.plateau_nb_lignes),
                            range(Conventions.plateau_nb_colonnes)):

            # Trait horizontal pour chaque nouvelle ligne
            if y == 0:
                print(self.trait_horizontal)
                print(" {}".format(next(iter_label_lignes)), end="")

            case = Case.instances[x, y]
            print(" |", case, end="")

            # Affichage de la barre verticale droite du tableau:
            if y == 9:
                print(" |")
        # Affichage de la dernière ligne horizontale
        print(self.trait_horizontal + "\n\n")

    def tester_fin_jeu(self):
        """Permet de tester si le jeu est terminé ou non"""
        if len(Navire.cases_occupees - self.cases_jouees) == 0:
            print("Bravo. Le jeu est terminé !")
            return True

        return False

    def jouer_un_coup(self):
        """Permet de gérer la saisie d'un coup à jouer"""
        while True:
            nom_case = demander_saisie_case(
                "Choisissez une case (lettre + chiffre)")
            # Retrouver la case à partir de son nom
            case = Case.instances[nom_case]
            # Tester si la case a déjà été jouée
            if case.jouee:
                print("Cette case a déjà été jouée, merci d'en choisir une autre",
                      file=sys.stderr)
            else:
                case.jouer()
                break


def jouer_une_partie():
    """Algorithme d'une partie"""
    # On crée un tableau de jeu vide

    plateau = Plateau()

    while True:
        plateau.afficher()

        plateau.jouer_un_coup()

        if plateau.tester_fin_jeu():
            # Si le jeu est terminé, on quitte la fonction
            plateau.afficher()
            return


def choisir_de_rejouer():
    return demander_saisie_oui_ou_non(
        "Souhaitez-vous refaire une nouvelle partie ? [o/n]")


def jouer():
    while True:
        jouer_une_partie()

        if not choisir_de_rejouer():
            return

