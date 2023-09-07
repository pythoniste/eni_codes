import sys

from itertools import cycle, chain

from saisie import (
    demander_saisie_nombre_borne,
    demander_saisie_oui_ou_non,
)


JOUEURS = ["X", "O"]


def jouer_un_coup(tableau, joueur):
    """Permet de gérer la saisie d'un coup à jouer"""
    while True:
        ligne = demander_saisie_nombre_borne(
            "Joueur {}, choisissez la ligne".format(joueur), 1, 3) - 1
        colonne = demander_saisie_nombre_borne(
            "Joueur {}, choisissez la colonne".format(joueur), 1, 3) - 1

        if tableau[ligne][colonne] != " ":
            print("Cette case a déjà été jouée, merci d'en choisir une autre",
                  file=sys.stderr)
        else:
            tableau[ligne][colonne] = joueur
            return tableau


TRAIT_HORIZONTAL = " " + "+---" * 3 + "+"


def afficher_tableau(tableau):
    for ligne in tableau:
        print(TRAIT_HORIZONTAL)
        for case in ligne:
            print(" |", case, end="")
        print("|")
    print(TRAIT_HORIZONTAL + "\n\n")


def tester_fin_jeu(tableau):
    """Permet de tester si le jeu est terminé ou non"""

    # Tester les lignes
    for ligne in tableau:
        if ligne[0] == ligne[1] == ligne[2] != " ":
            print("Le joueur {} a gagné".format(ligne[0]))
            return True

    # Tester les colonnes
    for colonne in zip(*tableau):
        if colonne[0] == colonne[1] == colonne[2] != " ":
            print("Le joueur {} a gagné".format(colonne[0]))
            return True

    # Tester les diagonales
    if tableau[0][0] == tableau[1][1] == tableau[2][2] != " " or\
       tableau[2][0] == tableau[1][1] == tableau[0][2] != " ":
        print("Le joueur {} a gagné".format(tableau[1][1]))
        return True

    # Tester qu'il reste encore des coups à jouer
    for case in chain(*tableau):
        if case == " ":
            return False
    else:
        print("Le jeu s'est terminé sur un match nul!")
        return True


def jouer_une_partie():
    """Algorithme d'une partie"""
    # On crée un tableau de jeu vide
    tableau = [[" "] * 3 for _ in range(3)]
    # >>> a=[[""] * 3] for _ in range(3)]
    # >>> a[0] is a[1]
    # False

    for joueur in cycle(JOUEURS):
        afficher_tableau(tableau)

        # Tour par tour, chaque joueur joue son coup
        tableau = jouer_un_coup(tableau, joueur)

        if tester_fin_jeu(tableau):
            # Si le jeu est terminé, on quitte la fonction
            afficher_tableau(tableau)
            return


def choisir_de_rejouer():
    return demander_saisie_oui_ou_non(
        "Souhaitez-vous refaire une nouvelle partie ? [o/n]")


def jouer():
    while True:
        jouer_une_partie()

        if not choisir_de_rejouer():
            return
