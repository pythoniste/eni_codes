import sys

from itertools import cycle

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
        print(" |")
    print(TRAIT_HORIZONTAL + "\n\n")


def tester_fin_jeu(tableau):
    """Permet de tester si le jeu est terminé ou non"""
    if tableau[0][0] != " ":
        return True


def jouer_une_partie():
    """Algorithme d'une partie"""
    # On crée un tableau de jeu vide
    tableau = [[" "] * 3] * 3
    # >>> a=[[""] * 3] * 3
    # >>> a[0] is a[1]
    # True

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
