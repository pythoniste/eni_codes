import sys

from itertools import product
from random import shuffle

from saisie import (
    demander_saisie_nombre_borne,
    demander_saisie_oui_ou_non,
)


TAILLES = [(2, 3), (4, 4), (4, 4), (4, 6), (4, 6)]
ORDINAUX = [0x2600, 0x2654, 0x263D, 0x2654, 0x2648]

# https://fr.wikipedia.org/wiki/Table_des_caract%C3%A8res_Unicode/U2600
CARTE_A_TROUVER = chr(0x2610)


def jouer_un_coup(taille, dictionnaire, lettres_trouvees):
    """Permet de gérer la saisie d'un coup à jouer"""
    while True:
        ligne1 = demander_saisie_nombre_borne(
            "ligne de la première carte", 1, taille[0]) - 1
        colonne1 = demander_saisie_nombre_borne(
            "colonne de la première carte", 1, taille[1]) - 1
        if dictionnaire[ligne1, colonne1] in lettres_trouvees:
            print("Cette case a déjà été jouée, merci d'en choisir une autre",
                  file=sys.stderr)
        else:
            break
    print("La première case est {}".format(dictionnaire[ligne1, colonne1]))

    while True:
        ligne2 = demander_saisie_nombre_borne(
            "ligne de la seconde carte", 1, taille[0]) - 1
        colonne2 = demander_saisie_nombre_borne(
            "colonne de la seconde carte", 1, taille[1]) - 1
        if dictionnaire[ligne2, colonne2] in lettres_trouvees:
            print("Cette case a déjà été jouée, merci d'en choisir une autre",
                  file=sys.stderr)
        elif ligne1 == ligne2 and colonne1 == colonne2:
            print("Vous avez choisi deux fois la même case, merci d'en changer",
                  file=sys.stderr)
        else:
            break
    print("La seconde case est {}".format(dictionnaire[ligne2, colonne2]))

    if dictionnaire[ligne1, colonne1] == dictionnaire[ligne2, colonne2]:
        print("Vous venez de trouver deux cartes identiques.")
        return dictionnaire[ligne1, colonne1]
    print("Vous n'avez pas trouvé de nouvelle carte.")


def afficher_tableau(taille, dictionnaire, lettres_trouvees):
    trait_horizontal = " " + "+---" * taille[1] + "+"
    for (x, y) in product(range(taille[0]), range(taille[1])):
        # Trait horizontal pour chaque nouvelle ligne
        if y == 0:
            print(trait_horizontal)

        # Retrouver la bonne case
        case = dictionnaire[x, y]

        # Cacher éventuellement, puis afficher la case, comme précédemment
        if case not in lettres_trouvees:
            case = CARTE_A_TROUVER
        print(" |", case, end="")

        # Affichage de la barre verticale droite du tableau:
        if y == taille[1] - 1:
            print(" |")
    # Affichage de la dernière ligne horizontale
    print(trait_horizontal + "\n\n")


def tester_fin_jeu(taille, lettres_trouvees):
    """Permet de tester si le jeu est terminé ou non"""
    if len(lettres_trouvees) >= int(taille[0] * taille[1] / 2):
        print("Bravo. Le jeu est terminé !")
        return True

    return False


def creer_dictionnaire(taille, ordinal):
    liste = list(product(range(taille[0]), range(taille[1])))
    shuffle(liste)
    dictionnaire = {}
    for index, coordonnee in enumerate(liste):
        dictionnaire[coordonnee] = chr(ordinal)
        if index % 2 == 1:
            ordinal += 1
    return dictionnaire


def jouer_une_partie(taille, ordinal):
    """Algorithme d'une partie"""
    # On crée un tableau de jeu vide
    dictionnaire = creer_dictionnaire(taille, ordinal)

    lettres_trouvees = []

    while True:
        afficher_tableau(taille, dictionnaire, lettres_trouvees)

        lettre = jouer_un_coup(taille, dictionnaire, lettres_trouvees)
        if lettre is not None:
            lettres_trouvees.append(lettre)

        if tester_fin_jeu(taille, lettres_trouvees):
            # Si le jeu est terminé, on quitte la fonction
            afficher_tableau(taille, dictionnaire, lettres_trouvees)
            return


def choisir_de_rejouer():
    return demander_saisie_oui_ou_non(
        "Souhaitez-vous refaire une nouvelle partie ? [o/n]")


def choisir_niveau():
    return demander_saisie_nombre_borne(
            "Quel est le niveau souhaité", 1, len(TAILLES)) - 1


def jouer():
    while True:
        niveau = choisir_niveau()

        taille = TAILLES[niveau]
        ordinal = ORDINAUX[niveau]

        jouer_une_partie(taille, ordinal)

        if not choisir_de_rejouer():
            return

