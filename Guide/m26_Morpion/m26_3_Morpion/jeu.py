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


def situations_a_tester(liste):
    """Renvoie l'ensemble des situations qui génèrent une victoire"""

    # Renvoyer les trois lignes:
    yield liste[:3]
    yield liste[3:6]
    yield liste[6:9]
    # Renvoyer les trois colonnes:
    yield liste[::3]
    yield liste[1::3]
    yield liste[2::3]
    # Renvoyer les deux diagonales:
    yield liste[::4]
    yield liste[2:8:2]


def tester_fin_jeu(tableau):
    """Permet de tester si le jeu est terminé ou non"""
    # Aplatir la liste
    liste = list(chain.from_iterable(tableau))

    for situation in situations_a_tester(liste):
        if situation[0] == situation[1] == situation[2] != " ":
            print("Le joueur {} a gagné".format(situation[0]))
            return True

    if " " not in liste:
        print("Le jeu s'est terminé sur un match nul!")
        return True

    return False


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
