import sys

from itertools import product, repeat
from functools import reduce
from random import choice, random

from saisie import (
    demander_saisie_oui_ou_non,
    demander_saisie_case,
)


LONGUEURS_BATEAUX = [2, 3, 3, 4, 4, 5]
ORDINAL = 0x2680

CASE_NON_JOUE = chr(0x2610)
CASE_TOUCHE = chr(0x2611)
CASE_BLANC = chr(0x2612)


def jouer_un_coup(cases_jouees):
    """Permet de gérer la saisie d'un coup à jouer"""
    while True:
        case = demander_saisie_case(
            "Choisissez une case (lettre + chiffre)")
        if case in cases_jouees:
            print("Cette case a déjà été jouée, merci d'en choisir une autre",
                  file=sys.stderr)
        else:
            return case


def afficher_tableau(lettres, chiffres, cases, navires,
                     cases_occupees, cases_jouees):

    trait_horizontal = " --" + "+---" * 10 + "+"

    print("   |", " | ".join(chiffres), "|")

    iter_lettres = iter(lettres)

    for coordonnee in cases:
        # Trait horizontal pour chaque nouvelle ligne
        if coordonnee[1] == "0":
            print(trait_horizontal)
            print(" {}".format(next(iter_lettres)), end="")

        # Retrouver la bonne case
        if coordonnee not in cases_jouees:
            case = CASE_NON_JOUE
        elif coordonnee in cases_occupees:
            case = CASE_TOUCHE
        else:
            case = CASE_BLANC

        print(" |", case, end="")

        # Affichage de la barre verticale droite du tableau:
        if coordonnee[1] == "9":
            print(" |")
    # Affichage de la dernière ligne horizontale
    print(trait_horizontal + "\n\n")


def tester_fin_jeu(cases_jouees, cases_occupees):
    """Permet de tester si le jeu est terminé ou non"""
    if len(cases_occupees - cases_jouees) == 0:
        print("Bravo. Le jeu est terminé !")
        return True

    return False


def creer_navires():
    navires = []
    for longueur in LONGUEURS_BATEAUX:
        # Un bateau est représenté par deux coordonnées: lettre et nombre
        # Ces deux coordonnées sont interchangeables:
        #    > l'une est fixe
        #    > l'autre varie du début à la fin du bateau

        while True:
            # choisir la coordonnée fixe du bateau
            print("Navire len {}, parmi {} et {}".format(longueur, list(range(10)), list(range(11-longueur))))
            rang = choice(range(10))
            # Choisir la coordonnée du début du bateau
            premier = choice(range(11-longueur))

            # Déterminer maintenant qui sera la lettre et qui sera le nombre
            if random() > 0.5:
                # Le navire est horizontal
                lettre = chr(65 + rang)
                chiffres = [str(x) for x in range(premier, premier + longueur)]
                # Créer le navire
                navire = {ligne + colonne for ligne, colonne in product(repeat(lettre, longueur), chiffres)}
            else:
                # Le navire est vertical
                chiffre = str(rang)
                lettres = [chr(65 + x) for x in range(premier, premier + longueur)]
                # Créer le navire
                navire = {ligne + colonne for ligne, colonne in product(lettres, repeat(chiffre, longueur))}

            for existant in navires:
                if navire.intersection(existant):
                    # Une case du navire se recoupe avec un navire existant
                    # La navire n'est pas bien placé, on le replace
                    break  # break relatif au "for existant in navires:"
            else:
                navires.append(navire)
                break  # break relatif au "while True:"

    return navires


def jouer_une_partie():
    """Algorithme d'une partie"""
    # On crée un tableau de jeu vide
    lettres = [chr(x) for x in range(65, 75)]
    chiffres = [str(x) for x in range(10)]
    cases = ["".join(x) for x in product(lettres, chiffres)]

    navires = creer_navires()
    print(navires)
    cases_occupees = set(reduce(set.union, navires))

    cases_jouees = set()

    while True:
        afficher_tableau(lettres, chiffres, cases, navires,
                         cases_occupees, cases_jouees)

        case = jouer_un_coup(cases_jouees)
        cases_jouees.add(case)
        if case in cases_occupees:
            for navire in navires:
                if case in navire:
                    # On a trouvé le navire touché
                    if len(navire - cases_jouees) == 0:
                        print("Coulé !!")
                    else:
                        print("Touché !")
                    # On a trouvé le navire, pas la peine de regarder les autres
                    break
        else:
            print("Dans l'eau !")

        if tester_fin_jeu(cases_jouees, cases_occupees):
            # Si le jeu est terminé, on quitte la fonction
            afficher_tableau(lettres, chiffres, cases, navires,
                             cases_occupees, cases_jouees)
            return


def choisir_de_rejouer():
    return demander_saisie_oui_ou_non(
        "Souhaitez-vous refaire une nouvelle partie ? [o/n]")


def jouer():
    while True:
        jouer_une_partie()

        if not choisir_de_rejouer():
            return

