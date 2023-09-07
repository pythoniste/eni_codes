import sys

from itertools import product
from random import shuffle

from saisie import (
    demander_saisie_nombre_borne,
    demander_saisie_oui_ou_non,
    demander_saisie_case,
)


TAILLES = [(2, 3), (4, 4), (4, 4), (4, 6), (4, 6)]
ORDINAUX = [0x2600, 0x2654, 0x263D, 0x2654, 0x2648]

# https://fr.wikipedia.org/wiki/Table_des_caract%C3%A8res_Unicode/U2600
CARTE_A_TROUVER = chr(0x2610)


def jouer_un_coup(taille, dictionnaire, lettres_trouvees):
    """Permet de gérer la saisie d'un coup à jouer"""
    while True:
        case1 = demander_saisie_case(
            "Choisissez une première case (lettre + chiffre)")
        if dictionnaire[case1] in lettres_trouvees:
            print("Cette case a déjà été jouée, merci d'en choisir une autre",
                  file=sys.stderr)
        else:
            break
    print("La première case est {}".format(dictionnaire[case1]))

    while True:
        case2 = demander_saisie_case(
            "Choisissez une seconde case (lettre + chiffre)")
        if dictionnaire[case2] in lettres_trouvees:
            print("Cette case a déjà été jouée, merci d'en choisir une autre",
                  file=sys.stderr)
        elif case1 == case2:
            print("Vous avez choisi deux fois la même case, merci d'en changer",
                  file=sys.stderr)
        else:
            break
    print("La seconde case est {}".format(dictionnaire[case2]))

    if dictionnaire[case1] == dictionnaire[case2]:
        print("Vous venez de trouver deux cartes identiques.")
        return dictionnaire[case1]
    print("Vous n'avez pas trouvé de nouvelle carte.")


def afficher_tableau(taille, dictionnaire, lettres_trouvees):
    lettres = [chr(x) for x in range(65, 65 + taille[0])]
    chiffres = [str(x) for x in range(taille[1])]

    trait_horizontal = " --" + "+---" * taille[1] + "+"

    print("   |", " | ".join(chiffres), "|")

    iter_lettres = iter(lettres)

    for coordonnee in ["".join(x) for x in product(lettres, chiffres)]:
        # Trait horizontal pour chaque nouvelle ligne
        if coordonnee[1] == "0":
            print(trait_horizontal)
            print(" {}".format(next(iter_lettres)), end="")

        # Retrouver la bonne case
        case = dictionnaire[coordonnee]

        # Cacher éventuellement, puis afficher la case, comme précédemment
        if case not in lettres_trouvees:
            case = CARTE_A_TROUVER
        print(" |", case, end="")

        # Affichage de la barre verticale droite du tableau:
        if coordonnee[1] == str(taille[1] - 1):
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
    lettres = [chr(x) for x in range(65, 65 + taille[0])]
    chiffres = [str(x) for x in range(taille[1])]
    liste = ["".join(x) for x in product(lettres, chiffres)]
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
