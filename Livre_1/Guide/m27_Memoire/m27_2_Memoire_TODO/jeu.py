import sys

from itertools import cycle, chain
from random import shuffle

from saisie import (
    demander_saisie_nombre_borne,
    demander_saisie_oui_ou_non,
    demander_saisie_lettre,
    demander_saisie_mot,
)


TAILLES = [(2, 3), (4, 4), (4, 4), (4, 6), (4, 6)]
ORDINAUX = [0x2600, 0x2654, 0x263D, 0x2654, 0x2648]

# https://fr.wikipedia.org/wiki/Table_des_caract%C3%A8res_Unicode/U2600
CARTE_A_TROUVER = chr(0x2610)


def jouer_un_coup(taille, tableau, cartes_trouvees):
    """Permet de gérer la saisie d'un coup à jouer"""
    while True:
        # TODO: demander la saisie des coordonnées, soit de la ligne et colonne
        # S'inspirer du jeu de morpion
        ligne1 = 1
        colonne1 = 1
        break
        # TODO: Si la carte a déjà été trouvé, on recommence la saisie.
        # TODO: Sinon, on quitte la boucle infinie: on a ce que l'on veut
    print("La première case est {}".format(tableau[ligne1][colonne1]))

    while True:
        # TODO: Tout de suite, on demande la saisie d'une seconde case
        ligne2 = 1
        colonne2 = 2
        break
        # TODO: Si la carte a déjà été trouvé, on recommence la saisie 2.
        # TODO: Si la carte 2 est la même que la carte 1, on recommence 2.
        # TODO: Sinon, on quitte la boucle infinie: on a ce que l'on veut
    print("La seconde case est {}".format(tableau[ligne2][colonne2]))

    # Si les deux cases sont identiques, on a trouvé une carte
    if tableau[ligne1][colonne1] == tableau[ligne2][colonne2]:
        print("Vous venez de trouver deux cartes identiques.")
        return tableau[ligne1][colonne1]
    # Sinon, on n'a pas trouvé de carte, elles restent face cachées.
    print("Vous n'avez pas trouvé de nouvelle carte.")


def afficher_tableau(taille, tableau, cartes_trouvees):
    trait_horizontal = " " + "+---" * taille[1] + "+"
    for ligne in tableau:
        print(trait_horizontal)
        for case in ligne:
            if case not in cartes_trouvees:
                case = CARTE_A_TROUVER
            print(" |", case, end="")
        print(" |")
    print(trait_horizontal + "\n\n")


def tester_fin_jeu(taille, cartes_trouvees):
    """Permet de tester si le jeu est terminé ou non"""
    # TODO: Si toutes les cartes sont retournées, alors on a gagné le jeu
    return False


def creer_tableau(taille, ordinal):
    return []  # TODO: Créer un tableau contenant deux fois chaque carte (et mélangées)


def jouer_une_partie(taille, ordinal):
    """Algorithme d'une partie"""
    # On crée un tableau de jeu vide
    tableau = creer_tableau(taille, ordinal)

    cartes_trouvees = []

    while True:
        afficher_tableau(taille, tableau, cartes_trouvees)

        carte = jouer_un_coup(taille, tableau, cartes_trouvees)
        if carte is not None:
            cartes_trouvees.append(carte)

        if tester_fin_jeu(taille, cartes_trouvees):
            # Si le jeu est terminé, on quitte la fonction
            afficher_tableau(taille, tableau, cartes_trouvees)
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

