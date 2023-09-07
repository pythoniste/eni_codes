import sys

from random import shuffle

from saisie import (
    demander_saisie_nombre_borne,
    demander_saisie_oui_ou_non,
)


TAILLES = [(2, 3), (4, 4), (4, 4), (4, 6), (4, 6)]
ORDINAUX = [0x2600, 0x2654, 0x263D, 0x2654, 0x2648]

# https://fr.wikipedia.org/wiki/Table_des_caract%C3%A8res_Unicode/U2600
CARTE_A_TROUVER = chr(0x2610)


def jouer_un_coup(taille, tableau, cartes_trouvees):
    """Permet de gérer la saisie d'un coup à jouer"""
    while True:
        ligne1 = demander_saisie_nombre_borne(
            "ligne de la première carte", 1, taille[0]) - 1
        colonne1 = demander_saisie_nombre_borne(
            "colonne de la première carte", 1, taille[1]) - 1
        if tableau[ligne1][colonne1] in cartes_trouvees:
            print("Cette case a déjà été jouée, merci d'en choisir une autre",
                  file=sys.stderr)
        else:
            break
    print("La première case est {}".format(tableau[ligne1][colonne1]))

    while True:
        ligne2 = demander_saisie_nombre_borne(
            "ligne de la seconde carte", 1, taille[0]) - 1
        colonne2 = demander_saisie_nombre_borne(
            "colonne de la seconde carte", 1, taille[1]) - 1
        if tableau[ligne2][colonne2] in cartes_trouvees:
            print("Cette case a déjà été jouée, merci d'en choisir une autre",
                  file=sys.stderr)
        elif ligne1 == ligne2 and colonne1 == colonne2:
            print("Vous avez choisi deux fois la même case, merci d'en changer",
                  file=sys.stderr)
        else:
            break
    print("La seconde case est {}".format(tableau[ligne2][colonne2]))

    if tableau[ligne1][colonne1] == tableau[ligne2][colonne2]:
        print("Vous venez de trouver deux cartes identiques.")
        return tableau[ligne1][colonne1]
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
    if len(cartes_trouvees) >= int(taille[0] * taille[1] / 2):
        print("Bravo. Le jeu est terminé !")
        return True

    return False


def creer_tableau(taille, ordinal):
    x, y = taille
    liste = [chr(x) for x in range(ordinal, ordinal + int(x * y / 2))] * 2
    shuffle(liste)
    return [liste[y*n:y*n+y] for n in range(x)]


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

